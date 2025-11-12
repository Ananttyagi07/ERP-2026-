from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentPromotionViewSet

router = DefaultRouter()
router.register(r'promotions', StudentPromotionViewSet, basename='student-promotion')

urlpatterns = [
    path('', include(router.urls)),
]
