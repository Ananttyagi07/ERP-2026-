from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentAttendanceViewSet, TeacherAttendanceViewSet,
    EmployeeAttendanceViewSet, AbsentEmailLogViewSet, AbsentSMSLogViewSet
)

router = DefaultRouter()
router.register(r'students', StudentAttendanceViewSet, basename='student-attendance')
router.register(r'teachers', TeacherAttendanceViewSet, basename='teacher-attendance')
router.register(r'employees', EmployeeAttendanceViewSet, basename='employee-attendance')
router.register(r'absent-emails', AbsentEmailLogViewSet, basename='absent-email-log')
router.register(r'absent-sms', AbsentSMSLogViewSet, basename='absent-sms-log')

urlpatterns = [
    path('', include(router.urls)),
]
