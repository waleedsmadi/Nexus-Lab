from django.db import models
from accounts.models import AuthUser
from product.models import Product
from django.db.models import Q, F


class OrderStatus(models.TextChoices):
    Pending = "pending", "Pending"
    Shipped = "shipped", "Shipped"
    Delivered = "Delivered", "delivered"
    Cancelled = "Cancelled", "cancelled"


class Order(models.Model):
    user = models.ForeignKey(
        to=AuthUser,
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,
        blank=True,
        verbose_name='User'
    )

    total_price = models.DecimalField(verbose_name='Total Price', max_digits=15, decimal_places=2)
    total_quantity = models.IntegerField(verbose_name='Total Quantity')
    status = models.CharField(max_length=20, verbose_name='Status', choices=OrderStatus.choices, default=OrderStatus.Pending)
    is_paid = models.BooleanField(verbose_name='Is Paid', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')


    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(name='chk_total_price_order', condition=Q(total_price__gt=0)),
            models.CheckConstraint(name="chk_total_quantity_order", condition=Q(total_quantity__gt=0)),
            models.CheckConstraint(name="chk_status_order", condition=~Q(status__in=[OrderStatus.Shipped, OrderStatus.Delivered]) | Q(is_paid=True))
        ]


    def __str__(self):
        return f'{self.user.username} - {self.total_price}'




class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Order'
    )

    product = models.ForeignKey(
        to=Product,
        on_delete=models.SET_NULL,
        related_name='order_items',
        verbose_name='Product',
        null=True,
        blank=True,
    )

    quantity = models.IntegerField(verbose_name='Quantity')
    price_at_purchase = models.DecimalField(verbose_name='Price At Purchase', max_digits=10, decimal_places=2)


    class Meta:
        constraints = [
            models.CheckConstraint(name='chk_quantity_order_item', condition=Q(quantity__gt=0)),
            models.CheckConstraint(name='chk_price_at_purchase_order_item', condition=Q(price_at_purchase__gt=0)),
        ]

    def __str__(self):
        return f"Order: {self.order.id}"