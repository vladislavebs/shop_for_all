from functools import wraps


def decorate(cls: object):
    decorators_configs = getattr(cls, "decorators")

    for method, decorators in decorators_configs.items():
        cls_method = getattr(cls, method)

        for decorator in reversed(decorators):
            # noinspection PyBroadException
            try:
                cls_method = decorator(cls_method)
            except Exception:
                pass

        setattr(cls, method, cls_method)

    return cls


def validate(serializer):
    def decorator(view_func):
        func_kwargs = getattr(view_func, "kwargs", {})
        fields = func_kwargs.get("fields", [])

        for index, field in enumerate(fields):
            if field[0] == "client":
                fields = list(fields)
                field = list(fields[index])

                if len(field) > 3:
                    field[3] = True
                else:
                    field.append(True)

                fields[index] = tuple(field)
                setattr(view_func, "kwargs", {**func_kwargs, "fields": tuple(fields)})
                break

        def wrapper(obj, request, *args, **kwargs):
            client_serializer = serializer(data=request.query_params)
            client_serializer.is_valid(raise_exception=True)

            return view_func(obj, request, *args, **kwargs)

        return wraps(view_func)(wrapper)

    return decorator
