"""Teachers URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, TeacherViewSet, TeacherLectureViewSet, RatingViewSet

app_name = 'teachers'

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'lectures', TeacherLectureViewSet, basename='lecture')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]
