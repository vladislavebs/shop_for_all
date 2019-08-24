from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter as Router

import products.views as products_views
from shop_for_all import settings
from shop_for_all.helpers.drf_yasg import docs_with_ui, docs_without_ui

router = Router(trailing_slash=False)
router.register("categories", products_views.CategoriesView, basename="category")
router.register("products", products_views.ProductsView, basename="product")

urlpatterns = [
    path("", docs_with_ui),
    path("docs_schema", docs_without_ui),
    path("admin/", admin.site.urls),
    *router.urls,
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
