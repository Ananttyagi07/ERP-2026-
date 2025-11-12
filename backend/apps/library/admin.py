"""
Django admin configuration for library
"""
from django.contrib import admin
from .models import Book, LibraryMember, BookIssue, EBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'book_id', 'isbn_no', 'author', 'quantity']
    list_filter = ['created_at']
    search_fields = ['title', 'book_id', 'isbn_no']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(LibraryMember)
class LibraryMemberAdmin(admin.ModelAdmin):
    list_display = ['student', 'library_id', 'is_active']
    list_filter = ['created_at']
    search_fields = ['student', 'library_id', 'is_active']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'issue_date', 'due_date', 'return_date']
    list_filter = ['created_at']
    search_fields = ['book', 'member', 'issue_date']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(EBook)
class EBookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn_no', 'subject']
    list_filter = ['created_at']
    search_fields = ['title', 'author', 'isbn_no']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


