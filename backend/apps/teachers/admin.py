"""Teachers admin"""
from django.contrib import admin
from .models import Teacher, TeacherLecture, Rating

# NOTE: Department admin is now in apps/colleges/admin.py

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'department', 'designation', 'joining_date']
    search_fields = ['user__email', 'user__username']
    list_filter = ['department', 'joining_date']

@admin.register(TeacherLecture)
class TeacherLectureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'teacher', 'lecture_date', 'lecture_type']
    search_fields = ['title']
    list_filter = ['lecture_type', 'lecture_date']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'rating_type', 'rating_value', 'created_at']
    list_filter = ['rating_type', 'created_at']
