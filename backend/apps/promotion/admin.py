from django.contrib import admin
from .models import StudentPromotion

@admin.register(StudentPromotion)
class StudentPromotionAdmin(admin.ModelAdmin):
    list_display = ['student', 'from_class', 'to_class', 'session_from', 'session_to', 'promotion_date']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['from_class', 'to_class', 'promotion_date']
