from django.db import models
from accounts.models import AuthUser
from product.models import Product
# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(
        to=AuthUser,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comments",
    )

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='comments',
        related_query_name='comments'
    )

    text = models.TextField(verbose_name='Comment', max_length=500)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True)




    class Meta:
        ordering = ['-created_at']
        

    def __str__(self):
        return self.user.get_full_name()