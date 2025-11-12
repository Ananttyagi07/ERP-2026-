"""
URL Configuration for payroll
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalaryGradeViewSet, SalaryPaymentViewSet

app_name = 'payroll'

router = DefaultRouter()
router.register(r'salary-grades', SalaryGradeViewSet, basename='salary-grades')
router.register(r'salary-payments', SalaryPaymentViewSet, basename='salary-payments')

urlpatterns = [
    path('', include(router.urls)),
]
