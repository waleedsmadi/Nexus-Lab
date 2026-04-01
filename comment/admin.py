from django.contrib import admin
from .models import Comment


# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'product']
    search_fields = ['user', 'product']
    raw_id_fields = ['user', 'product']
    list_display_links = ['user', 'product']
    