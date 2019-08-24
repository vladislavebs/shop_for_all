import tempfile
import typing
from functools import reduce

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.backends.db import SessionStore
from django.db import models
from django.template.loader import render_to_string

USER_MODEL: AbstractUser = get_user_model()


def choices_to_list(choices):
    return list(map(lambda choice: choice[0], choices))


def new_session(data, expiry=1800):
    session = SessionStore()
    session.update(data)
    session.set_expiry(expiry)
    session.create()
    return session


def format_foreign_key_limit(*limits):
    def _format_foreign_key_limit(foreign_limit, limit):
        app, model = limit
        q = models.Q(app_label=app, model=model)

        if not foreign_limit:
            return q

        return foreign_limit | q

    return reduce(_format_foreign_key_limit, limits, None)


def get_temp(
    suffix: str = None, prefix: str = None, mode: str = "r+", encoding: str = "utf-8"
) -> typing.IO:
    if "b" in mode:
        encoding = None

    return tempfile.NamedTemporaryFile(
        mode, suffix=suffix, prefix=prefix, encoding=encoding
    )


def render_to_temp(template: str, context: dict) -> typing.IO:
    file: typing.IO = get_temp(suffix=".html")

    content: str = render_to_string(template, context)

    file.write(content)
    file.seek(0)

    return file
