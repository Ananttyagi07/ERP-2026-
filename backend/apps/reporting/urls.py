"""
URL Configuration for reporting
"""
from django.urls import path
from .views import StudentReportView, AttendanceReportView, FinanceReportView

app_name = 'reporting'

urlpatterns = [
    path('student/', StudentReportView.as_view(), name='student-report'),
    path('attendance/', AttendanceReportView.as_view(), name='attendance-report'),
    path('finance/', FinanceReportView.as_view(), name='finance-report'),
]
