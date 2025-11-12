from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentTypeViewSet, OnlineAdmissionViewSet, StudentActivityViewSet

router = DefaultRouter()
router.register(r'types', StudentTypeViewSet, basename='student-type')
router.register(r'online-admissions', OnlineAdmissionViewSet, basename='online-admission')
router.register(r'activities', StudentActivityViewSet, basename='student-activity')

urlpatterns = [
    path('', include(router.urls)),
]
