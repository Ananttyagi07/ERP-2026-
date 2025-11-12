"""
Django admin configuration for transport
"""
from django.contrib import admin
from .models import Vehicle, TransportRoute, RouteStop, TransportMember


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_number', 'vehicle_model', 'driver_name', 'driver_contact']
    list_filter = ['created_at']
    search_fields = ['vehicle_number', 'vehicle_model', 'driver_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(TransportRoute)
class TransportRouteAdmin(admin.ModelAdmin):
    list_display = ['route_name', 'route_start', 'route_end']
    list_filter = ['created_at']
    search_fields = ['route_name', 'route_start', 'route_end']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ['route', 'vehicle', 'stop_name', 'stop_fare']
    list_filter = ['created_at']
    search_fields = ['route', 'vehicle', 'stop_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(TransportMember)
class TransportMemberAdmin(admin.ModelAdmin):
    list_display = ['student', 'route', 'stop', 'vehicle']
    list_filter = ['created_at']
    search_fields = ['student', 'route', 'stop']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


