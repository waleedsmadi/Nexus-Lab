from django.urls import path
from . import views


app_name = 'comment'



urlpatterns = [
    path('comments/add/<str:product_slug>/', views.add_comment, name='add_comment_url'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment_url'),
    path('comments/edit/<int:comment_id>/', views.edit_comment, name='edit_comment_url'),
]
