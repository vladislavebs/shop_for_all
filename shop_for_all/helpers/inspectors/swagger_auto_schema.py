from drf_yasg.inspectors import SwaggerAutoSchema as _SwaggerAutoSchema


class SwaggerAutoSchema(_SwaggerAutoSchema):
    @property
    def auto_schema(self) -> dict:
        view = self.view
        action = getattr(view, "action", "")
        method = getattr(view, action, None)
        return getattr(method, "_swagger_auto_schema", {})

    def should_filter(self):
        show_filters = self.auto_schema.get("show_filters")

        if show_filters is not None:
            return getattr(self.view, "filter_backends", None) and show_filters

        return super(SwaggerAutoSchema, self).should_filter()

    def get_filter_parameters(self):
        filter_backends = self.auto_schema.get("filter_backends")

        if filter_backends:
            fields = []
            for filter_backend in filter_backends:
                fields += (
                    self.probe_inspectors(
                        inspectors=self.filter_inspectors,
                        method_name="get_filter_parameters",
                        obj=filter_backend(),
                    )
                    or []
                )

            return fields

        return super(SwaggerAutoSchema, self).get_filter_parameters()
