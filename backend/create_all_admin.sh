#!/bin/bash
# Create admin registrations for all 9 modules

cd /home/anant/ERP-MAIN-PROJECT/backend

python3 << 'PYTHON_EOF'
# Create all admin.py files

# Student Management Admin
with open('apps/student_management/admin.py', 'w') as f:
    f.write('''from django.contrib import admin
from .models import StudentType, OnlineAdmission, StudentActivity

@admin.register(StudentType)
class StudentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'created_at']
    search_fields = ['name']
    list_filter = ['college', 'created_at']

@admin.register(OnlineAdmission)
class OnlineAdmissionAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'email', 'phone', 'school_class', 'status', 'created_at']
    search_fields = ['student_name', 'email', 'phone']
    list_filter = ['status', 'school_class', 'created_at']

@admin.register(StudentActivity)
class StudentActivityAdmin(admin.ModelAdmin):
    list_display = ['student', 'school_class', 'section', 'activity_date']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['school_class', 'section', 'activity_date']
''')

# Attendance Admin
with open('apps/attendance/admin.py', 'w') as f:
    f.write('''from django.contrib import admin
from .models import (
    StudentAttendance, TeacherAttendance, EmployeeAttendance,
    AbsentEmailLog, AbsentSMSLog
)

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'school_class', 'section', 'attendance_date', 'status']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['status', 'attendance_date', 'school_class']

@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'attendance_date', 'status']
    search_fields = ['teacher__user__first_name', 'teacher__user__last_name']
    list_filter = ['status', 'attendance_date']

@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'attendance_date', 'status']
    search_fields = ['employee__user__first_name', 'employee__user__last_name']
    list_filter = ['status', 'attendance_date']

@admin.register(AbsentEmailLog)
class AbsentEmailLogAdmin(admin.ModelAdmin):
    list_display = ['receiver_type', 'receiver_email', 'absent_date', 'created_at']
    search_fields = ['receiver_email']
    list_filter = ['receiver_type', 'absent_date']

@admin.register(AbsentSMSLog)
class AbsentSMSLogAdmin(admin.ModelAdmin):
    list_display = ['receiver_type', 'receiver_phone', 'absent_date', 'created_at']
    search_fields = ['receiver_phone']
    list_filter = ['receiver_type', 'absent_date']
''')

# Card Generation Admin
with open('apps/card_generation/admin.py', 'w') as f:
    f.write('''from django.contrib import admin
from .models import IDCardSetting, AdmitCardSetting

@admin.register(IDCardSetting)
class IDCardSettingAdmin(admin.ModelAdmin):
    list_display = ['college', 'card_school_name', 'created_at']
    search_fields = ['card_school_name']

@admin.register(AdmitCardSetting)
class AdmitCardSettingAdmin(admin.ModelAdmin):
    list_display = ['college', 'card_school_name', 'created_at']
    search_fields = ['card_school_name']
''')

# Online Exam Admin
with open('apps/online_exam/admin.py', 'w') as f:
    f.write('''from django.contrib import admin
from .models import ExamInstruction, QuestionBank, OnlineExam, OnlineExamResult

@admin.register(ExamInstruction)
class ExamInstructionAdmin(admin.ModelAdmin):
    list_display = ['title', 'college', 'created_at']
    search_fields = ['title']

@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ['subject', 'question_type', 'question_level', 'mark']
    search_fields = ['question']
    list_filter = ['question_type', 'question_level', 'subject']

@admin.register(OnlineExam)
class OnlineExamAdmin(admin.ModelAdmin):
    list_display = ['exam_title', 'subject', 'exam_date', 'publish_status']
    search_fields = ['exam_title']
    list_filter = ['publish_status', 'exam_date', 'subject']

@admin.register(OnlineExamResult)
class OnlineExamResultAdmin(admin.ModelAdmin):
    list_display = ['exam', 'student', 'obtained_mark', 'status', 'submitted_at']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['status', 'exam']
''')

# Exam Management Admin
with open('apps/exam_management/admin.py', 'w') as f:
    f.write('''from django.contrib import admin
from .models import Grade, ExamTerm, ExamSchedule, ExamSuggestion, ExamAttendanceRecord

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['grade_name', 'point', 'mark_from', 'mark_to']
    search_fields = ['grade_name']

@admin.register(ExamTerm)
class ExamTermAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'created_at']
    search_fields = ['name']

@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ['exam_term', 'subject', 'school_class', 'exam_date', 'exam_time']
    search_fields = ['subject__name']
    list_filter = ['exam_term', 'school_class', 'exam_date']

@admin.register(ExamSuggestion)
class ExamSuggestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'exam_term', 'subject', 'school_class']
    search_fields = ['title']
    list_filter = ['exam_term', 'subject']

@admin.register(ExamAttendanceRecord)
class ExamAttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['exam_schedule', 'student', 'status']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['status', 'exam_schedule']
''')

# Marks Admin
with open('apps/marks/admin.py', 'w') as f:
    f.write('''from django.contrib import admin
from .models import (
    ExamMark, MarkDistribution, ResultCard,
    MarkEmailLog, MarkSMSLog, ResultEmailLog, ResultSMSLog
)

@admin.register(ExamMark)
class ExamMarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_schedule', 'total_mark', 'grade', 'attendance_status']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['exam_schedule', 'attendance_status']

@admin.register(MarkDistribution)
class MarkDistributionAdmin(admin.ModelAdmin):
    list_display = ['exam_term', 'school_class', 'subject']
    list_filter = ['exam_term', 'school_class', 'subject']

@admin.register(ResultCard)
class ResultCardAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_term', 'obtained_marks', 'percentage', 'result_status', 'merit_position']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['exam_term', 'result_status']

@admin.register(MarkEmailLog)
class MarkEmailLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'receiver_email', 'exam_schedule', 'created_at']
    search_fields = ['receiver_email']

@admin.register(MarkSMSLog)
class MarkSMSLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'receiver_phone', 'exam_schedule', 'created_at']
    search_fields = ['receiver_phone']

@admin.register(ResultEmailLog)
class ResultEmailLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'receiver_email', 'exam_term', 'created_at']
    search_fields = ['receiver_email']

@admin.register(ResultSMSLog)
class ResultSMSLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'receiver_phone', 'exam_term', 'created_at']
    search_fields = ['receiver_phone']
''')

# Promotion Admin
with open('apps/promotion/admin.py', 'w') as f:
    f.write('''from django.contrib import admin
from .models import StudentPromotion

@admin.register(StudentPromotion)
class StudentPromotionAdmin(admin.ModelAdmin):
    list_display = ['student', 'from_class', 'to_class', 'session_from', 'session_to', 'promotion_date']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['from_class', 'to_class', 'promotion_date']
''')

# Certificates Admin
with open('apps/certificates/admin.py', 'w') as f:
    f.write('''from django.contrib import admin
from .models import CertificateType, CertificateGeneration

@admin.register(CertificateType)
class CertificateTypeAdmin(admin.ModelAdmin):
    list_display = ['certificate_name', 'school_name', 'created_at']
    search_fields = ['certificate_name', 'school_name']

@admin.register(CertificateGeneration)
class CertificateGenerationAdmin(admin.ModelAdmin):
    list_display = ['certificate_type', 'student', 'school_class', 'created_at']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['certificate_type', 'school_class']
''')

# Inventory Admin
with open('apps/inventory/admin.py', 'w') as f:
    f.write('''from django.contrib import admin
from .models import Supplier, Warehouse, InventoryCategory, Product, Purchase, Sale, ProductIssue

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
    search_fields = ['name', 'phone', 'email']

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['title', 'address']
    search_fields = ['title']

@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'college']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'warehouse', 'unit_price', 'quantity']
    search_fields = ['name']
    list_filter = ['category', 'warehouse']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['product', 'supplier', 'quantity', 'total_price', 'purchase_date']
    search_fields = ['product__name']
    list_filter = ['purchase_date', 'supplier']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer_name', 'quantity', 'total_price', 'invoice_no', 'sale_date']
    search_fields = ['product__name', 'customer_name', 'invoice_no']
    list_filter = ['sale_date']

@admin.register(ProductIssue)
class ProductIssueAdmin(admin.ModelAdmin):
    list_display = ['product', 'issue_type', 'quantity', 'issue_to', 'issue_date']
    search_fields = ['product__name', 'issue_to']
    list_filter = ['issue_type', 'issue_date']
''')

print("✓ Created student_management admin")
print("✓ Created attendance admin")
print("✓ Created card_generation admin")
print("✓ Created online_exam admin")
print("✓ Created exam_management admin")
print("✓ Created marks admin")
print("✓ Created promotion admin")
print("✓ Created certificates admin")
print("✓ Created inventory admin")
print("\n✅ All admin registrations created successfully!")
PYTHON_EOF

echo ""
echo "========================================================================"
echo "✅ ALL ADMIN REGISTRATIONS CREATED FOR 9 MODULES!"
echo "========================================================================"
