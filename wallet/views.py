from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.views.decorators.clickjacking import xframe_options_sameorigin
from .models import Transaction, Wallet
from django.core.paginator import Paginator
from .forms import WalletForm
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit


@login_required
@ratelimit(key='post:request.user.username', rate='5/m', block=True)
def create_wallet(request):
    if request.user.wallet:
        return redirect('wallet:wallet_url', request.user.username)
    

    if request.method == "POST":
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            wallet.save()
            return redirect('wallet:wallet_url', request.user.username)
        else:
            return render(request, 'wallet/create_wallet.html', {'form': form})

    else:
        form = WalletForm()
        return render(request, 'wallet/create_wallet.html', {'form': form})



@login_required
def view_wallet(request, username):
    if request.user.username != username:
        raise PermissionDenied
    
    exists = True
    try:
        Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        exists = False

    
    
    return render(request, 'wallet/wallet.html', {"is_exists": exists})


@login_required
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