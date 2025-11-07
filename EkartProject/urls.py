"""
URL configuration for EkartProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from ekartApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomeView.as_view(),name="home_view"),

    path('category/<int:id>',views.CatListView.as_view(),name='category_list'),
    
    path('detail/<int:id>',views.ProductDetailView.as_view(),name="detail_view"),
    path('add-to-cart/<int:id>',views.AddToCartView.as_view(),name='add_to_cart'),
    path('cart-list',views.CartListView.as_view(),name='cart_list'),
    path('cart-delete/<int:id>',views.CartDeleteView.as_view(),name='cart_delete'),
    path('place-order',views.PlaceOrderView.as_view(),name='place_order'),
    path('buy-now-place-order/<int:id>',views.BuyNowPlaceOrderView.as_view(),name='buy_now_place_order'),
    path('order-list',views.OrderListView.as_view(),name='order_list'),
    path('order-cancel/<int:id>',views.OrderCancelView.as_view(),name='order_cancel'),
    path('payment-success/', views.payment_success, name='payment_success'),

    path('adminapp/',include('adminApp.urls')),


    path('register',views.RegisterView.as_view(),name='register'),
    path('login',views.LoginView.as_view(),name='login'),
    path('logout',views.LogoutView.as_view(),name='logout'),

    path('--',views.DemoView.as_view(),name='demo'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

