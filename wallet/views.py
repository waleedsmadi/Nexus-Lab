from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.views.decorators.clickjacking import xframe_options_sameorigin
from .models import Transaction, Wallet, TransactionType
from django.core.paginator import Paginator
from .forms import DepoistWalletForm
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.db import transaction

@login_required
@ratelimit(key='user', method='POST', rate='5/m', block=True)
def create_wallet(request):
    if hasattr(request.user, 'wallet'):
            return redirect('wallet:wallet_url', request.user.username)
    
    if request.method == "POST":
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        return redirect('wallet:wallet_url', request.user.username)

        
    return render(request, 'wallet/create_wallet.html')



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




@login_required
@ratelimit(key="user", method="POST", rate="5/m", block=True)
@transaction.atomic
def deposit(request, username):
    if request.user.username != username:
        raise PermissionDenied
    

    # Check in all cases whether he has a wallet or not
    if not hasattr(request.user, 'wallet'):
            return redirect('wallet:wallet_url', username=username)
    

    if request.method == "POST":
        form = DepoistWalletForm(request.POST)
        if form.is_valid():

            # get the wallet for this user by (select_for_update) To avoid interference problems
            wallet = Wallet.objects.select_for_update().get(user=request.user)

            
            # if there is wallet and the data is valid >> deposit
            deposit_amount = form.cleaned_data.get('balance')
            old_balance = wallet.balance
            wallet.balance += deposit_amount
            wallet.save()


            # create transaction
            Transaction.objects.create(
                wallet=wallet,
                amount=deposit_amount,
                transaction_type=TransactionType.Deposit,
                description=f"Depoist for User: #{request.user.id}"
            )
            messages.success(request, f'The balance has been updated from {old_balance}$ - to {wallet.balance}$')
            return redirect('wallet:depoist_url', username=request.user.username)
        return render(request, 'wallet/depoist.html', {'form': form})
    
    else:
        form = DepoistWalletForm()
    return render(request, 'wallet/depoist.html', {'form': form})

    
