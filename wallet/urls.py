from django.urls import path
from . import views

app_name = 'wallet'


urlpatterns = [
    path('<str:username>/', views.view_wallet, name='wallet_url'),
    path('transactions/<str:username>/', views.view_transactions, name='transactions_url'),
]
