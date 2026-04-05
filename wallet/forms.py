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

        if balance is None:
            raise ValidationError('Error: Please enter a valid value.!')


        try:
            balance = Decimal(str(balance))
        except (ValueError, TypeError, InvalidOperation):
            raise ValidationError('Error: The amount must be a number.!')

        if balance < 5:
            raise ValidationError('Error: The balance should be at least 5$ or more.!')
        
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
        if amount is None:
            raise ValidationError('Error: Please enter a valid value.!')
        try:
            amount = Decimal(str(amount))
        except (ValueError, TypeError, InvalidOperation):
            raise ValidationError('Error: The amount must be a number.!')

        if amount < 5:
            raise ValidationError('Error: The amount should be at least 5$ or more.!')

        return amount