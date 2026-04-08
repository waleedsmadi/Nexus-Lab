from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'vulner_type', 'severity', 'status', 'created_at', 'updated_at']
    list_filter = ['vulner_type', 'severity', 'status']
    search_fields = ['title', 'user', 'vulner_type']
    list_display_links = ['vulner_type']
    raw_id_fields = ['user']