from django.db import models
from django.db.models import Q
from accounts.models import AuthUser
from django.db.models.functions import Length
# Create your models here.
import secrets
from string import digits


def gen_wallet_number():
    random_number = ''.join(secrets.choice(digits) for _ in range(12))
    return random_number




class Wallet(models.Model):
    wallet_number = models.CharField(max_length=12, unique=True, editable=False, verbose_name='Wallet Number')
    user = models.OneToOneField(
        to=AuthUser,
        on_delete=models.CASCADE,
        related_name='wallet',
        related_query_name='wallet'
    )

    balance = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='Balance', default=0.00)

    class Meta:
        constraints = [
            models.CheckConstraint(name='chk_wallet_balance', condition=Q(balance__gte=0.00)),
            models.CheckConstraint(name='chk_wallet_wallet_number', condition=Q(wallet_number__length=12)),
            
        ]

    def __str__(self):
        return self.user.username
    

    def save(self, *args, **kwargs):
        if not self.wallet_number:

            while True:
                rand_number = gen_wallet_number()
                if not Wallet.objects.filter(wallet_number=rand_number).exists():
                    self.wallet_number = rand_number
                    break
        super().save(*args, **kwargs)
    




class TransactionType(models.TextChoices):
    Deposit = "deposit", "Deposit"
    Withdraw = "withdraw", "Withdraw"
    Purchase = "purchase", "Purchase"


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions', verbose_name='Wallet')
    amount = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='Amount')
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices, verbose_name='Transaction Type')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(name='chk_transaction_amount', condition=Q(amount__gte=5.00))
        ]

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"