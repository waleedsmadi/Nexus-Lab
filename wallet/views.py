from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.views.decorators.clickjacking import xframe_options_sameorigin
from .models import Transaction, Wallet

def view_wallet(request, username):
    if request.user.username != username:
        raise PermissionDenied
    
    
    return render(request, 'wallet/wallet.html')



@xframe_options_sameorigin
def view_transactions(request, username):
    if request.user.username != username:
        raise PermissionDenied
    
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        return redirect('wallet:wallet_url', request.user.username)
    

    transactions = Transaction.objects.filter(wallet=wallet)
    
    return render(request, 'wallet/transactions.html', {'transactions': transactions})