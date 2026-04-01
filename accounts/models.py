from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import secrets
import string



# Generation a unique username
def gen_username(first_name, last_name):
    first_name = slugify(first_name.lower()) or "user"
    last_name = slugify(last_name.lower()) or "member"
    random_digits = ''.join(secrets.choice(string.digits) for _ in range(8))
    username = f'{first_name}.{last_name}{random_digits}'
    return username



# AuthUser model based on built-in User model
class AuthUser(AbstractUser):
    email = models.EmailField(verbose_name='Email', unique=True)
    img = models.ImageField(upload_to='users/images/%Y-%m-%d',verbose_name='Image', null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    class Meta:
        ordering = ['-date_joined']
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural='users'



    # Save a unique username when create a new user 
    def save(self, *args, **kwargs):
        if not self.username:

            
            while True:
                new_username = gen_username(self.first_name, self.last_name)
                if not AuthUser.objects.filter(username=new_username).exists():
                    self.username = new_username
                    break


        super().save(*args, **kwargs)


    def __str__(self):
        return self.username
