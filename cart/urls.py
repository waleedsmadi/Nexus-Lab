from django.urls import path
from . import views


app_name = 'cart'


urlpatterns = [
    path('', views.view_cart, name='cart_view_url'),
    path('add/<int:product_id>/', views.add_cart, name='add_cart_url'),
    path('delete/<int:product_id>/', views.delete_cart, name='delete_cart_url'),
    path('minus/<int:product_id>/', views.minus_cart, name='minus_cart_url'),
]
