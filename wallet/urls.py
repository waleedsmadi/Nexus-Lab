from django.urls import path
from . import views

app_name = 'wallet'


urlpatterns = [
    path('create-wallet/', views.create_wallet, name='create_wallet_url'),
    path('transactions/<str:username>/', views.view_transactions, name='transactions_url'),
    path('<str:username>/', views.view_wallet, name='wallet_url'),
]
