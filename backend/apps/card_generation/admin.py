from django.contrib import admin
from .models import IDCardSetting, AdmitCardSetting

@admin.register(IDCardSetting)
class IDCardSettingAdmin(admin.ModelAdmin):
    list_display = ['college', 'card_school_name', 'created_at']
    search_fields = ['card_school_name']

@admin.register(AdmitCardSetting)
class AdmitCardSettingAdmin(admin.ModelAdmin):
    list_display = ['college', 'card_school_name', 'created_at']
    search_fields = ['card_school_name']
