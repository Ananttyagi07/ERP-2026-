"""
URL Configuration for accounting
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiscountViewSet, FeeTypeViewSet, InvoiceViewSet, PaymentViewSet, IncomeHeadViewSet, IncomeViewSet, ExpenditureHeadViewSet, ExpenditureViewSet

app_name = 'accounting'

router = DefaultRouter()
router.register(r'discounts', DiscountViewSet, basename='discounts')
router.register(r'fee-types', FeeTypeViewSet, basename='fee-types')
router.register(r'invoices', InvoiceViewSet, basename='invoices')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'income-heads', IncomeHeadViewSet, basename='income-heads')
router.register(r'incomes', IncomeViewSet, basename='incomes')
router.register(r'expenditure-heads', ExpenditureHeadViewSet, basename='expenditure-heads')
router.register(r'expenditures', ExpenditureViewSet, basename='expenditures')

urlpatterns = [
    path('', include(router.urls)),
]
