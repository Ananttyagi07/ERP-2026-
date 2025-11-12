from django.contrib import admin
from .models import CertificateType, CertificateGeneration

@admin.register(CertificateType)
class CertificateTypeAdmin(admin.ModelAdmin):
    list_display = ['certificate_name', 'school_name', 'created_at']
    search_fields = ['certificate_name', 'school_name']

@admin.register(CertificateGeneration)
class CertificateGenerationAdmin(admin.ModelAdmin):
    list_display = ['certificate_type', 'student', 'school_class', 'created_at']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['certificate_type', 'school_class']
