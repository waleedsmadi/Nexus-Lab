from django import forms
from .models import Wallet
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation



class DepositWalletForm(forms.Form):
    balance = forms.DecimalField(
        required=True,
        max_digits=11,
        decimal_places=2,
        help_text='',
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Balance...',
            "step": '0.01',
        })
    )



    def clean_balance(self):
        balance = self.cleaned_data.get('balance')


        if balance and balance < 5:
            raise ValidationError('Error: The balance should be at least 5$ or more.!')

        if balance and balance < 0:
            raise ValidationError('Error: The balance should be greater than zero.')
        
        return balance



class WithdrawalWalletForm(forms.Form):
    amount = forms.DecimalField(
        required=True,
        max_digits=11,
        decimal_places=2,
        help_text='',
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Amount...',
        }),
    )



    def clean_amount(self):
        amount = self.cleaned_data.get('amount')


        if amount and amount < 0:
            raise ValidationError('Error: The amount should be greater than zero.')

        return amount