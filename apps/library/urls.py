"""
URL Configuration for library
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, LibraryMemberViewSet, BookIssueViewSet, EBookViewSet

app_name = 'library'

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='books')
router.register(r'library-members', LibraryMemberViewSet, basename='library-members')
router.register(r'book-issues', BookIssueViewSet, basename='book-issues')
router.register(r'ebooks', EBookViewSet, basename='ebooks')

urlpatterns = [
    path('', include(router.urls)),
]
