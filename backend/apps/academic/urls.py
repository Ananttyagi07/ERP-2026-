"""Academic URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (SchoolClassViewSet, ClassSectionViewSet, SubjectViewSet,
                    SyllabusViewSet, StudyMaterialViewSet)

app_name = 'academic'

router = DefaultRouter()
router.register(r'classes', SchoolClassViewSet, basename='school-class')
router.register(r'sections', ClassSectionViewSet, basename='section')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'syllabi', SyllabusViewSet, basename='syllabus')
router.register(r'study-materials', StudyMaterialViewSet, basename='study-material')

urlpatterns = [
    path('', include(router.urls)),
]
