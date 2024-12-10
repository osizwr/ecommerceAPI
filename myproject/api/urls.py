from django.urls import path
from .views import UsersListView, UserListView, UserCreateView
from .views import OrdersListView, OrdersCreateView, OrdersRetrieveUpdateDestroy
from .views import CartItemListView, CartItemCreateView
from .views import CheckoutView

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
]