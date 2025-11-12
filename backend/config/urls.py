"""
URL configuration for University ERP project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Core API Endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/roles/', include('apps.roles.urls')),
    path('api/colleges/', include('apps.colleges.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/finance/', include('apps.finance.urls')),
    path('api/reports/', include('apps.reports.urls')),

    # Superadmin Module Endpoints (Phase 1)
    path('api/superadmin/', include('apps.superadmin.urls')),
    path('api/templates/', include('apps.templates.urls')),
    path('api/front-office/', include('apps.front_office.urls')),
    path('api/hr/', include('apps.hr.urls')),
    path('api/teachers/', include('apps.teachers.urls')),
    path('api/leave/', include('apps.leave_management.urls')),
    path('api/academic/', include('apps.academic.urls')),
    path('api/live-classes/', include('apps.live_classes.urls')),
    path('api/students/', include('apps.students.urls')),
    path('api/guardians/', include('apps.guardians.urls')),

    # Extended Feature Endpoints (Phase 2)
    path('api/student-management/', include('apps.student_management.urls')),
    path('api/attendance/', include('apps.attendance.urls')),
    path('api/card-generation/', include('apps.card_generation.urls')),
    path('api/online-exam/', include('apps.online_exam.urls')),
    path('api/exam-management/', include('apps.exam_management.urls')),
    path('api/marks/', include('apps.marks.urls')),
    path('api/promotion/', include('apps.promotion.urls')),
    path('api/certificates/', include('apps.certificates.urls')),
    path('api/inventory/', include('apps.inventory.urls')),

    # Superadmin Phase 3 - Complete Feature Set
    path('api/asset-management/', include('apps.asset_management.urls')),
    path('api/library/', include('apps.library.urls')),
    path('api/transport/', include('apps.transport.urls')),
    path('api/messaging/', include('apps.messaging.urls')),
    path('api/communication/', include('apps.communication.urls')),
    path('api/complain/', include('apps.complain.urls')),
    path('api/announcement/', include('apps.announcement.urls')),
    path('api/scholarship/', include('apps.scholarship.urls')),
    path('api/event/', include('apps.event.urls')),
    path('api/payroll/', include('apps.payroll.urls')),
    path('api/accounting/', include('apps.accounting.urls')),
    path('api/reporting/', include('apps.reporting.urls')),
    path('api/media-gallery/', include('apps.media_gallery.urls')),
    path('api/frontend-cms/', include('apps.frontend_cms.urls')),
    path('api/miscellaneous/', include('apps.miscellaneous.urls')),
    path('api/subscription/', include('apps.subscription.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Django Debug Toolbar
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

# Custom admin site configuration
admin.site.site_header = "University ERP Administration"
admin.site.site_title = "ERP Admin"
admin.site.index_title = "Welcome to University ERP Management Portal"
