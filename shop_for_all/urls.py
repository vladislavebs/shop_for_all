from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_extensions.routers import ExtendedSimpleRouter as Router

import products.views as products_views
import shops.views as shops_views
import users.views as users_views
from shop_for_all import settings
from shop_for_all.helpers.drf_yasg import docs_with_ui, docs_without_ui

product_endpoint = dict(prefix="products", viewset=products_views.ProductsView)
category_endpoint = dict(prefix="categories", viewset=products_views.CategoriesView)
shop_endpoint = dict(prefix="shops", viewset=shops_views.StoresView)


router = Router(trailing_slash=False)
router.register(**category_endpoint, basename="category")
router.register(**product_endpoint, basename="product")
router.register(prefix="users", viewset=users_views.UserView, basename="user")
router.register(prefix="user/shop", viewset=shops_views.UserStoreView, basename="user_shop")


shops_router = router.register(**shop_endpoint, basename="shop")
shops_router.register(
    **product_endpoint, basename="shop-product", parents_query_lookups=["product_store"]
)

urlpatterns = [
    path("", docs_with_ui),
    path("docs_schema", docs_without_ui),
    path("admin/", admin.site.urls),
    *router.urls,
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


# users_router.register(
#     prefix="store/products",
#     viewset=products_views.ProductsView,
#     basename="shop-product",
#     parents_query_lookups=["product_store__store__user"],
# )

# shops_router.register(
#     **category_endpoint,
#     basename="shop-category",
#     parents_query_lookups=["category_store"]
# )
