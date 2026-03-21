#!/usr/bin/env python3
"""Generate all URL patterns for ERP modules"""

URLS_FILES = {
    'apps/superadmin/urls.py': '''"""Superadmin URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuperAdminViewSet

app_name = 'superadmin'

router = DefaultRouter()
router.register(r'superadmins', SuperAdminViewSet, basename='superadmin')

urlpatterns = [
    path('', include(router.urls)),
]
''',

    'apps/templates/urls.py': '''"""Templates URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SMSTemplateViewSet, EmailTemplateViewSet

app_name = 'templates'

router = DefaultRouter()
router.register(r'sms-templates', SMSTemplateViewSet, basename='sms-template')
router.register(r'email-templates', EmailTemplateViewSet, basename='email-template')

urlpatterns = [
    path('', include(router.urls)),
]
''',

    'apps/front_office/urls.py': '''"""Front Office URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (VisitorPurposeViewSet, VisitorInfoViewSet, CallLogViewSet,
                    PostalDispatchViewSet, PostalReceiveViewSet)

app_name = 'front_office'

router = DefaultRouter()
router.register(r'visitor-purposes', VisitorPurposeViewSet, basename='visitor-purpose')
router.register(r'visitor-info', VisitorInfoViewSet, basename='visitor-info')
router.register(r'call-logs', CallLogViewSet, basename='call-log')
router.register(r'postal-dispatches', PostalDispatchViewSet, basename='postal-dispatch')
router.register(r'postal-receives', PostalReceiveViewSet, basename='postal-receive')

urlpatterns = [
    path('', include(router.urls)),
]
''',

    'apps/hr/urls.py': '''"""HR URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DesignationViewSet, EmployeeViewSet

app_name = 'hr'

router = DefaultRouter()
router.register(r'designations', DesignationViewSet, basename='designation')
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]
''',

    'apps/teachers/urls.py': '''"""Teachers URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, TeacherViewSet, TeacherLectureViewSet, RatingViewSet

app_name = 'teachers'

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'lectures', TeacherLectureViewSet, basename='lecture')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]
''',

    'apps/leave_management/urls.py': '''"""Leave Management URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveTypeViewSet, LeaveApplicationViewSet

app_name = 'leave_management'

router = DefaultRouter()
router.register(r'leave-types', LeaveTypeViewSet, basename='leave-type')
router.register(r'leave-applications', LeaveApplicationViewSet, basename='leave-application')

urlpatterns = [
    path('', include(router.urls)),
]
''',

    'apps/academic/urls.py': '''"""Academic URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (SchoolClassViewSet, ClassSectionViewSet, SubjectViewSet,
                    SyllabusViewSet, StudyMaterialViewSet)

app_name = 'academic'

router = DefaultRouter()
router.register(r'classes', SchoolClassViewSet, basename='school-class')
router.register(r'sections', ClassSectionViewSet, basename='section')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'syllabi', SyllabusViewSet, basename='syllabus')
router.register(r'study-materials', StudyMaterialViewSet, basename='study-material')

urlpatterns = [
    path('', include(router.urls)),
]
''',

    'apps/live_classes/urls.py': '''"""Live Classes URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LiveClassTypeViewSet, LiveClassViewSet, AssignmentViewSet

app_name = 'live_classes'

router = DefaultRouter()
router.register(r'live-class-types', LiveClassTypeViewSet, basename='live-class-type')
router.register(r'live-classes', LiveClassViewSet, basename='live-class')
router.register(r'assignments', AssignmentViewSet, basename='assignment')

urlpatterns = [
    path('', include(router.urls)),
]
''',

    'apps/students/urls.py': '''"""Students URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StudentParentViewSet

app_name = 'students'

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'student-parents', StudentParentViewSet, basename='student-parent')

urlpatterns = [
    path('', include(router.urls)),
]
''',

    'apps/guardians/urls.py': '''"""Guardians URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuardianViewSet

app_name = 'guardians'

router = DefaultRouter()
router.register(r'guardians', GuardianViewSet, basename='guardian')

urlpatterns = [
    path('', include(router.urls)),
]
''',
}

print("🚀 Generating URL patterns...")
print("=" * 60)

for filepath, content in URLS_FILES.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ {filepath}")

print("\n✅ All URL patterns created!")
print("=" * 60)
