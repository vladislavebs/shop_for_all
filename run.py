import os

import django

from shop_for_all.settings import BASIC_APP

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{BASIC_APP}.settings")

django.setup()
