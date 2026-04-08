from django.urls import path
from . import views

app_name = 'vdp'



urlpatterns = [
    path('submission/', views.submission, name='submission_url'),
    path('submission/view/', views.submission_view, name='submission_view_url'),
]
