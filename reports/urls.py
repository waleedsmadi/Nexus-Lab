from django.urls import path
from . import views

app_name = 'reports'



urlpatterns = [
    path('', views.view_reports, name='reports_view_url'),
    path('create/', views.create_report, name='create_report_url'),
    
]
