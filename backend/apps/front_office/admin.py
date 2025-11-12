"""Front Office admin"""
from django.contrib import admin
from .models import VisitorPurpose, VisitorInfo, CallLog, PostalDispatch, PostalReceive

@admin.register(VisitorPurpose)
class VisitorPurposeAdmin(admin.ModelAdmin):
    list_display = ['id', 'purpose', 'created_at']
    search_fields = ['purpose']

@admin.register(VisitorInfo)
class VisitorInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'purpose', 'check_in_date', 'check_out_date']
    search_fields = ['name', 'phone', 'visitor_id']
    list_filter = ['check_in_date', 'meet_user_type']

@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'call_type', 'call_date']
    search_fields = ['name', 'phone']
    list_filter = ['call_type', 'call_date']

@admin.register(PostalDispatch)
class PostalDispatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'to_title', 'reference_number', 'dispatch_date']
    search_fields = ['to_title', 'reference_number']
    list_filter = ['dispatch_date']

@admin.register(PostalReceive)
class PostalReceiveAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_title', 'reference_number', 'receive_date', 'receiver_type']
    search_fields = ['from_title', 'reference_number']
    list_filter = ['receiver_type', 'receive_date']
