"""shop_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from shops.views import ShopImportViewSet, ShopStateViewSet, OpenShopViewSet
from contacts.views import ClientRegisterViewSet, ClientEmailConfirmViewSet, PasswordChangeViewSet
from orders.views import ClientBasketViewSet, UserOrderViewSet
from products.views import ProductViewSet
from categories.views import ProductCategoryViewSet
from django.contrib import admin
from rest_framework.authtoken import views
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

partner_router = DefaultRouter()
partner_router.register('import', ShopImportViewSet, basename='shop_import')
partner_router.register('states', ShopStateViewSet, basename='shops_states')
partner_router.register('orders', UserOrderViewSet, basename='shop_orders')
partner_router.register('pwd', PasswordChangeViewSet, basename='password_change')

client_router = DefaultRouter()
client_router.register('reg', ClientRegisterViewSet, basename='client_register')
client_router.register('confirm', ClientEmailConfirmViewSet, basename='client_confirm')
client_router.register('basket', ClientBasketViewSet, basename='basket')
client_router.register('orders', UserOrderViewSet, basename='client_orders')
client_router.register('pwd', PasswordChangeViewSet, basename='password_change')

shop_router = DefaultRouter()
shop_router.register('shops', OpenShopViewSet, basename='open_shops')
shop_router.register('products', ProductViewSet, basename='products')
shop_router.register('categories', ProductCategoryViewSet, basename='categories')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(shop_router.urls)),
    path('api/v1/auth/', views.obtain_auth_token),
    path('api/v1/partner/', include(partner_router.urls)),
    path('api/v1/client/', include(client_router.urls)),

    # Drf-spectacular module route. This route basically provides the schema.
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Drf-spectacular module route. And this route creates a UI out of the schema above.
    path('api/v1/ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]
