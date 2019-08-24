import calendar
import os
import subprocess
import sys
import time
import typing


def get_index(_list: iter, index: int, default: any = None) -> any:
    return _list[index] if len(_list) > index else default


def unpack(
    iterable: dict, *fields: typing.Iterable[str or typing.Iterable[str, str]]
) -> typing.Iterable[typing.Tuple]:
    return (
        iterable.get(field[0], field[1])
        if isinstance(field, tuple)
        else iterable.get(field)
        for field in fields
        if not isinstance(field, tuple)
        or (isinstance(field, tuple) and len(field) is 2)
    )


def timestamp():
    return calendar.timegm(time.gmtime())


def dict_if(cond, then, _else=None):
    if _else is None:
        _else = {}

    return then if cond else _else


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
