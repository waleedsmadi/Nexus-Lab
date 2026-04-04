from django import forms
from .models import Wallet





class WalletForm(forms.ModelForm):
    

    class Meta:
        model = Wallet
        fields = ['balance',]

        widgets = {
            'balance': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Balance',
                'step': "0.01",
                'max': "999999999.99",
                'min': '0',
            })
        }


    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.required = True