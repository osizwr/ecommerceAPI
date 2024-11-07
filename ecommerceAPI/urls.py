"""
URL configuration for ecommerceAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
"""
    path('', views.home, name=''),
    path('orders/', views.order, name=''),
    path('orders/<orderId>/', views.order, name=''),
    path('cart-items/', views.cart-item, name=''),
    path('checkout/', views.checkout, name=''),
    path('users/', views.user, name=''),
    path('users/<userId>', views.user, name=''),
"""

from django.contrib import admin
from django.urls import path
from myEcommerceApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
]
