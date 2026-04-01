from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.views.decorators.clickjacking import xframe_options_sameorigin

def view_wallet(request, username):
    if request.user.username != username:
        raise PermissionDenied
    
    
    return render(request, 'wallet/wallet.html')



@xframe_options_sameorigin
def view_transactions(request, username):
    if request.user.username != username:
        raise PermissionDenied
    
    
    return render(request, 'wallet/transactions.html')