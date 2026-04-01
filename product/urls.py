from django.urls import path
from . import views


app_name = 'product'


urlpatterns = [
    path('products/search/', views.search_products, name='search_products_url'),
    path('products/load-more-products/', views.load_more_products, name='load_more_products_url'),
    path('product/<str:the_slug>/', views.product, name='product_url'),
    path('products/<str:category>/', views.products, name='products_url'),
]
