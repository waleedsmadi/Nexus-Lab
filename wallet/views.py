from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.views.decorators.clickjacking import xframe_options_sameorigin
from .models import Transaction, Wallet
from django.core.paginator import Paginator


def view_wallet(request, username):
    if request.user.username != username:
        raise PermissionDenied
    
    exists = True
    try:
        Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        exists = False

    
    
    return render(request, 'wallet/wallet.html', {"is_exists": exists})



@xframe_options_sameorigin
def view_transactions(request, username):
    if request.user.username != username:
        raise PermissionDenied
    
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        return redirect('wallet:wallet_url', request.user.username)
    

    transactions = Transaction.objects.filter(wallet=wallet)
    paginator = Paginator(transactions, 8)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    page_obj.elided_pages = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    return render(request, 'wallet/transactions.html', {'page_obj': page_obj})