import calendar
import os
import subprocess
import sys
import time
import typing
from functools import reduce


def get_index(_list: iter, index: int, default: any = None) -> any:
    return _list[index] if len(_list) > index else default


GET_MAP = {
    list: get_index,
    dict: lambda _dict, field, default: _dict.get(field, default),
    type: getattr,
}


def default_get_method(obj, field, default):
    # noinspection PyBroadException
    try:
        return obj[field]
    except Exception:
        return default


def get(obj, field, default=None):
    method = GET_MAP.get(type(obj), default_get_method)
    return method(obj, field, default)


def get_item(iter_object: iter, path: str, default: any = None) -> any:
    value = iter_object

    for key in path.split("."):
        value = get(value, key, default)

        if value is default:
            break

    return value


def unpack(
    iterable: iter,
    *fields: typing.Iterable[str or typing.Iterable[str, str]],
    default: any = None,
) -> typing.Iterable[typing.Tuple]:
    def _unpack(unpacked: list, field: str):
        unpack_default = default

        if isinstance(field, tuple):
            field, unpack_default, *_ = field

        unpacked.append(
            (
                get_item(iterable, field, unpack_default)
                if "." in field
                else get(iterable, field, unpack_default)
            )
        )

        return unpacked

    return tuple(reduce(_unpack, fields, []))


def timestamp():
    return calendar.timegm(time.gmtime())


def dict_if(cond, then, _else=None):
    if _else is None:
        _else = {}

    return then if cond else _else


def hasattrs(obj: object, *attrs):
    return all(hasattr(obj, attr) for attr in attrs)


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def merge_ranges(ranges):
    """
    Merge overlapping and adjacent ranges and yield the merged ranges
    in order. The argument must be an iterable of pairs (start, stop).

        >>> list(merge_ranges([(5,7), (3,5), (-1,3)]))
        [(-1, 7)]
        >>> list(merge_ranges([(5,6), (3,4), (1,2)]))
        [(1, 2), (3, 4), (5, 6)]
        >>> list(merge_ranges([]))
        []
    """
    ranges = iter(sorted(ranges))
    current_start, current_stop = next(ranges)

    for start, stop in ranges:
        if start > current_stop:
            # Gap between segments: output current segment and start a new one.
            yield current_start, current_stop
            current_start, current_stop = start, stop
        else:
            # Segments adjacent or overlapping: merge.
            current_stop = max(current_stop, stop)

    yield current_start, current_stop


def get_location(executable):
    command = "where" if sys.platform == "win32" else "which"

    location = (
        subprocess.Popen([command, executable], stdout=subprocess.PIPE)
        .communicate()[0]
        .strip()
    )

    if not os.path.exists(location):
        raise IOError(f"No {executable} executable found.")

    return location
