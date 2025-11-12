from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExamMarkViewSet, MarkDistributionViewSet, ResultCardViewSet,
    MarkEmailLogViewSet, MarkSMSLogViewSet,
    ResultEmailLogViewSet, ResultSMSLogViewSet
)

router = DefaultRouter()
router.register(r'marks', ExamMarkViewSet, basename='exam-mark')
router.register(r'distributions', MarkDistributionViewSet, basename='mark-distribution')
router.register(r'result-cards', ResultCardViewSet, basename='result-card')
router.register(r'mark-emails', MarkEmailLogViewSet, basename='mark-email-log')
router.register(r'mark-sms', MarkSMSLogViewSet, basename='mark-sms-log')
router.register(r'result-emails', ResultEmailLogViewSet, basename='result-email-log')
router.register(r'result-sms', ResultSMSLogViewSet, basename='result-sms-log')

urlpatterns = [
    path('', include(router.urls)),
]
