from django.db import models
from django.db.models import Q, F
from django.utils.text import slugify









class Category(models.TextChoices):
    MOB = "MOB", "Mobiles"
    LAP = "LAP", "Laptops"
    TAB = "TAB", "Tablets" 
    MEN = "MEN", "Men Fashion"
    WMN = "WMN", "Women Fashion"
    TOY = "TOY", "Toyes"
    LIT = "LIT", "Lighting"


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title', unique=True)
    slug = models.SlugField(max_length=200, verbose_name='Slug', unique=True)
    description = models.TextField(max_length=500, verbose_name='Description')
    img = models.ImageField(upload_to='products/%Y-%m-%d', verbose_name='Image', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    quantity = models.IntegerField(verbose_name='Quantity')
    discount = models.IntegerField(verbose_name='Discount', default=0)
    category = models.CharField(max_length=6, verbose_name="Category", choices=Category.choices)
    available = models.BooleanField(verbose_name="Available", default=True)
    created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)


    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.CheckConstraint(name='chk_product_quantity', condition=Q(quantity__lte=10000)&Q(quantity__gte=0)),
            models.CheckConstraint(name='chk_product_price', condition=Q(price__gt=0)),
            models.CheckConstraint(name='chk_product_discount', condition=Q(discount__gte=0)&Q(discount__lt=F("price"))),
        ]
        db_table = 'product'



    @property
    def final_price(self):
        return self.price - self.discount
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        if self.quantity == 0:
            self.available = False
        else:
            self.available = True
        
        return super().save(*args, **kwargs)






    def __str__(self):
        return self.title




class ProductImage(models.Model):
    img = models.ImageField(upload_to='products/images/%Y%m%d', verbose_name='Product Image', null=True, blank=True)
    product = models.ForeignKey(
        to="Product",
        on_delete=models.CASCADE,
        related_name='images',
        related_query_name="images_query",
    )
    created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)



    

    def __str__(self):
        return self.product.title