from django.urls import path
from .views import UsersListView, UserListView, UserCreateView
from .views import OrdersListView, OrdersCreateView, OrdersRetrieveUpdateDestroy
from .views import CartItemListView, CartItemCreateView
from .views import CheckoutView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('users/', UsersListView.as_view(), name='UserListView'),
    path('users/create/', UserCreateView.as_view(), name='UserCreateView'),
    path('users/<uuid:userID>/', UserListView.as_view(), name='UserListView'),

    path('orders/', OrdersListView.as_view(), name='OrdersListView'),
    path('orders/create/', OrdersCreateView.as_view(), name='OrdersCreateView'),
    path('orders/<uuid:orderID>/', OrdersRetrieveUpdateDestroy.as_view(), name='OrdersRetrieveUpdateDestroy'),

    path('cart-items/create/', CartItemCreateView.as_view(), name='CartItemCreateView'),
    path('cart-items/<uuid:orderID>/', CartItemListView.as_view(), name='CartItemListView'),

    path('checkout/', CheckoutView.as_view(), name='CheckoutView'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]