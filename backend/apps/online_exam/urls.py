from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExamInstructionViewSet, QuestionBankViewSet,
    OnlineExamViewSet, OnlineExamResultViewSet
)

router = DefaultRouter()
router.register(r'instructions', ExamInstructionViewSet, basename='exam-instruction')
router.register(r'questions', QuestionBankViewSet, basename='question-bank')
router.register(r'exams', OnlineExamViewSet, basename='online-exam')
router.register(r'results', OnlineExamResultViewSet, basename='exam-result')

urlpatterns = [
    path('', include(router.urls)),
]
