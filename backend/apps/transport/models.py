"""Transport Management models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Vehicle(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Transport vehicles"""
    vehicle_number = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=255, blank=True)
    driver = models.CharField(max_length=255, blank=True)
    vehicle_license = models.CharField(max_length=100, blank=True)
    vehicle_contact = models.CharField(max_length=20)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'vehicles'
        unique_together = [['college', 'vehicle_number']]

    def __str__(self):
        return f"{self.vehicle_number} - {self.vehicle_model}"


class TransportRoute(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Transport routes"""
    route_name = models.CharField(max_length=255)
    route_start = models.CharField(max_length=255)
    route_end = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'transport_routes'

    def __str__(self):
        return self.route_name


class RouteStop(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Stops on transport routes"""
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE, related_name='stops')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='assigned_stops')
    stop_name = models.CharField(max_length=255)
    stop_km = models.DecimalField(max_digits=6, decimal_places=2)
    stop_fare = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'route_stops'

    def __str__(self):
        return f"{self.route.route_name} - {self.stop_name}"


class TransportMember(TimeStampedModel, CollegeIsolatedModel):
    """Students using transport"""
    student = models.OneToOneField('students.Student', on_delete=models.CASCADE, related_name='transport_membership')
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE, related_name='members')
    stop = models.ForeignKey(RouteStop, on_delete=models.CASCADE, related_name='members')

    class Meta:
        db_table = 'transport_members'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.route.route_name}"
