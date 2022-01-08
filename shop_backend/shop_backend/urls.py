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
from django.contrib import admin
from django.urls import path, include
from shops.views import ShopImportViewSet, ShopStateViewSet, ShopOrderViewSet
from contacts.views import UserRegisterViewSet
from products.views import ProductViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

partner_router = DefaultRouter()
partner_router.register('update', ShopImportViewSet, basename='shop_update')
partner_router.register('state', ShopStateViewSet, basename='shop_state')
partner_router.register('order', ShopOrderViewSet, basename='shop_orders')

common_router = DefaultRouter()
common_router.register('reg', UserRegisterViewSet, basename='user_register')

shop_router = DefaultRouter()
shop_router.register('products', ProductViewSet, basename='shop_products')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', views.obtain_auth_token),
    path('api/v1/', include(common_router.urls)),
    path('api/v1/', include(shop_router.urls)),
    path('api/v1/partner/', include(partner_router.urls)),
]
