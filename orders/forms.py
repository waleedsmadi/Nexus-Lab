from django import forms


class CheckOutForm(forms.Form):
    wallet_number = forms.CharField(
        required=True,
        label='',
        help_text='',
        max_length=12,
        min_length=12,
        widget=forms.TextInput(attrs={
            "class": 'form-control',
            "placeholder": "Your wallet number...",
        })
    )

    password = forms.CharField(
        required=True,
        max_length=255,
        help_text='',
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password...',
        })
    )


    