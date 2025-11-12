from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GradeViewSet, ExamTermViewSet, ExamScheduleViewSet,
    ExamSuggestionViewSet, ExamAttendanceRecordViewSet
)

router = DefaultRouter()
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'terms', ExamTermViewSet, basename='exam-term')
router.register(r'schedules', ExamScheduleViewSet, basename='exam-schedule')
router.register(r'suggestions', ExamSuggestionViewSet, basename='exam-suggestion')
router.register(r'attendance', ExamAttendanceRecordViewSet, basename='exam-attendance')

urlpatterns = [
    path('', include(router.urls)),
]
