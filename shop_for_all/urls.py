from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from shop_for_all import settings
from shop_for_all.helpers.drf_yasg import docs_with_ui, docs_without_ui

urlpatterns = [
    path("", docs_with_ui),
    path("docs_schema", docs_without_ui),
    path("admin", admin.site.urls),
    # *router.urls,
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
