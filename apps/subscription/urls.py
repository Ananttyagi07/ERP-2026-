"""
URL Configuration for subscription
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet, SubscriptionViewSet, SubscriptionPaymentViewSet

app_name = 'subscription'

router = DefaultRouter()
router.register(r'subscription-plans', SubscriptionPlanViewSet, basename='subscription-plans')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register(r'subscription-payments', SubscriptionPaymentViewSet, basename='subscription-payments')

urlpatterns = [
    path('', include(router.urls)),
]
