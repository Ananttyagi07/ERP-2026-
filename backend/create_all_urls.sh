#!/bin/bash
# Create URL patterns for all 9 modules

cd /home/anant/ERP-MAIN-PROJECT/backend

python3 << 'PYTHON_EOF'
# Create all URL files

# Student Management URLs
with open('apps/student_management/urls.py', 'w') as f:
    f.write('''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentTypeViewSet, OnlineAdmissionViewSet, StudentActivityViewSet

router = DefaultRouter()
router.register(r'types', StudentTypeViewSet, basename='student-type')
router.register(r'online-admissions', OnlineAdmissionViewSet, basename='online-admission')
router.register(r'activities', StudentActivityViewSet, basename='student-activity')

urlpatterns = [
    path('', include(router.urls)),
]
''')

# Attendance URLs
with open('apps/attendance/urls.py', 'w') as f:
    f.write('''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentAttendanceViewSet, TeacherAttendanceViewSet,
    EmployeeAttendanceViewSet, AbsentEmailLogViewSet, AbsentSMSLogViewSet
)

router = DefaultRouter()
router.register(r'students', StudentAttendanceViewSet, basename='student-attendance')
router.register(r'teachers', TeacherAttendanceViewSet, basename='teacher-attendance')
router.register(r'employees', EmployeeAttendanceViewSet, basename='employee-attendance')
router.register(r'absent-emails', AbsentEmailLogViewSet, basename='absent-email-log')
router.register(r'absent-sms', AbsentSMSLogViewSet, basename='absent-sms-log')

urlpatterns = [
    path('', include(router.urls)),
]
''')

# Card Generation URLs
with open('apps/card_generation/urls.py', 'w') as f:
    f.write('''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IDCardSettingViewSet, AdmitCardSettingViewSet

router = DefaultRouter()
router.register(r'id-card-settings', IDCardSettingViewSet, basename='id-card-setting')
router.register(r'admit-card-settings', AdmitCardSettingViewSet, basename='admit-card-setting')

urlpatterns = [
    path('', include(router.urls)),
]
''')

# Online Exam URLs
with open('apps/online_exam/urls.py', 'w') as f:
    f.write('''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExamInstructionViewSet, QuestionBankViewSet,
    OnlineExamViewSet, OnlineExamResultViewSet
)

router = DefaultRouter()
router.register(r'instructions', ExamInstructionViewSet, basename='exam-instruction')
router.register(r'questions', QuestionBankViewSet, basename='question-bank')
router.register(r'exams', OnlineExamViewSet, basename='online-exam')
router.register(r'results', OnlineExamResultViewSet, basename='exam-result')

urlpatterns = [
    path('', include(router.urls)),
]
''')

# Exam Management URLs
with open('apps/exam_management/urls.py', 'w') as f:
    f.write('''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GradeViewSet, ExamTermViewSet, ExamScheduleViewSet,
    ExamSuggestionViewSet, ExamAttendanceRecordViewSet
)

router = DefaultRouter()
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'terms', ExamTermViewSet, basename='exam-term')
router.register(r'schedules', ExamScheduleViewSet, basename='exam-schedule')
router.register(r'suggestions', ExamSuggestionViewSet, basename='exam-suggestion')
router.register(r'attendance', ExamAttendanceRecordViewSet, basename='exam-attendance')

urlpatterns = [
    path('', include(router.urls)),
]
''')

# Marks URLs
with open('apps/marks/urls.py', 'w') as f:
    f.write('''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExamMarkViewSet, MarkDistributionViewSet, ResultCardViewSet,
    MarkEmailLogViewSet, MarkSMSLogViewSet,
    ResultEmailLogViewSet, ResultSMSLogViewSet
)

router = DefaultRouter()
router.register(r'marks', ExamMarkViewSet, basename='exam-mark')
router.register(r'distributions', MarkDistributionViewSet, basename='mark-distribution')
router.register(r'result-cards', ResultCardViewSet, basename='result-card')
router.register(r'mark-emails', MarkEmailLogViewSet, basename='mark-email-log')
router.register(r'mark-sms', MarkSMSLogViewSet, basename='mark-sms-log')
router.register(r'result-emails', ResultEmailLogViewSet, basename='result-email-log')
router.register(r'result-sms', ResultSMSLogViewSet, basename='result-sms-log')

urlpatterns = [
    path('', include(router.urls)),
]
''')

# Promotion URLs
with open('apps/promotion/urls.py', 'w') as f:
    f.write('''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentPromotionViewSet

router = DefaultRouter()
router.register(r'promotions', StudentPromotionViewSet, basename='student-promotion')

urlpatterns = [
    path('', include(router.urls)),
]
''')

# Certificates URLs
with open('apps/certificates/urls.py', 'w') as f:
    f.write('''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CertificateTypeViewSet, CertificateGenerationViewSet

router = DefaultRouter()
router.register(r'types', CertificateTypeViewSet, basename='certificate-type')
router.register(r'generate', CertificateGenerationViewSet, basename='certificate-generation')

urlpatterns = [
    path('', include(router.urls)),
]
''')

# Inventory URLs
with open('apps/inventory/urls.py', 'w') as f:
    f.write('''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SupplierViewSet, WarehouseViewSet, InventoryCategoryViewSet,
    ProductViewSet, PurchaseViewSet, SaleViewSet, ProductIssueViewSet
)

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'categories', InventoryCategoryViewSet, basename='inventory-category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'purchases', PurchaseViewSet, basename='purchase')
router.register(r'sales', SaleViewSet, basename='sale')
router.register(r'issues', ProductIssueViewSet, basename='product-issue')

urlpatterns = [
    path('', include(router.urls)),
]
''')

print("✓ Created student_management URLs")
print("✓ Created attendance URLs")
print("✓ Created card_generation URLs")
print("✓ Created online_exam URLs")
print("✓ Created exam_management URLs")
print("✓ Created marks URLs")
print("✓ Created promotion URLs")
print("✓ Created certificates URLs")
print("✓ Created inventory URLs")
print("\n✅ All URL patterns created successfully!")
PYTHON_EOF

echo ""
echo "========================================================================"
echo "✅ ALL URL PATTERNS CREATED FOR 9 MODULES!"
echo "========================================================================"
