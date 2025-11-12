#!/usr/bin/env python
"""
Bulk ViewSet Permission Updater Script

This script automatically updates all ViewSets across the ERP system to:
1. Add BaseModelPermission for automatic permission enforcement
2. Add AuditLoggingMixin for automatic CRUD logging
3. Map to correct ACL module names

Usage:
    python scripts/update_viewsets_permissions.py --dry-run  # Preview changes
    python scripts/update_viewsets_permissions.py --apply    # Apply changes
    python scripts/update_viewsets_permissions.py --app student_management  # Update specific app
"""

import os
import sys
import re
import argparse
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ACL Module Mapping (from seed_permissions.py)
ACL_MODULE_MAPPING = {
    # Student Management
    'StudentViewSet': 'student',
    'GuardianViewSet': 'guardian',
    'StudentAttendanceViewSet': 'attendance',
    'StudentEnrollmentViewSet': 'enrollment',

    # Teacher Management
    'TeacherViewSet': 'teacher',
    'TeacherAttendanceViewSet': 'attendance',
    'TeacherAssignmentViewSet': 'teacher',

    # Staff Management
    'StaffViewSet': 'staff',
    'StaffAttendanceViewSet': 'attendance',

    # Academic
    'ClassViewSet': 'class',
    'SectionViewSet': 'section',
    'SubjectViewSet': 'subject',
    'SessionViewSet': 'session',
    'TimeTableViewSet': 'timetable',
    'PeriodViewSet': 'period',
    'HolidayViewSet': 'holiday',
    'EventViewSet': 'event',

    # Exam Management
    'ExamViewSet': 'exam',
    'ExamScheduleViewSet': 'exam',
    'ExamMarkViewSet': 'exam_mark',
    'GradeViewSet': 'grade',
    'ResultViewSet': 'result',
    'ReportCardViewSet': 'report',
    'ProgressReportViewSet': 'report',

    # Attendance
    'AttendanceViewSet': 'attendance',
    'LeaveRequestViewSet': 'leave',
    'LeaveApprovalViewSet': 'leave',

    # Library
    'BookViewSet': 'library',
    'BookIssueViewSet': 'library',
    'MemberViewSet': 'library',

    # Hostel
    'HostelViewSet': 'hostel',
    'RoomViewSet': 'hostel',
    'HostelAllocationViewSet': 'hostel',

    # Transport
    'VehicleViewSet': 'transport',
    'RouteViewSet': 'transport',
    'TransportAllocationViewSet': 'transport',

    # Fee Management
    'FeeStructureViewSet': 'fee',
    'FeeCollectionViewSet': 'fee',
    'FeePaymentViewSet': 'fee',
    'FeeReceiptViewSet': 'fee',
    'DiscountViewSet': 'fee',

    # Accounting
    'AccountViewSet': 'accounting',
    'TransactionViewSet': 'accounting',
    'ExpenseViewSet': 'expense',
    'IncomeViewSet': 'income',
    'BudgetViewSet': 'budget',
    'InvoiceViewSet': 'invoice',

    # HR & Payroll
    'PayrollViewSet': 'payroll',
    'SalaryViewSet': 'payroll',
    'LeaveManagementViewSet': 'leave',
    'DepartmentViewSet': 'department',
    'DesignationViewSet': 'designation',

    # Communication
    'NotificationViewSet': 'notification',
    'AnnouncementViewSet': 'notification',
    'MessageViewSet': 'messaging',
    'EmailTemplateViewSet': 'email',
    'SMSTemplateViewSet': 'sms',

    # Settings
    'GeneralSettingViewSet': 'setting',
    'SchoolSettingViewSet': 'setting',
    'SystemConfigViewSet': 'setting',

    # Reports
    'ReportViewSet': 'report',
    'AnalyticsViewSet': 'report',

    # User Management (Roles)
    'RoleViewSet': 'role',
    'PermissionViewSet': 'permission',
    'UserViewSet': 'user',

    # Inventory
    'InventoryViewSet': 'inventory',
    'ItemViewSet': 'inventory',
    'PurchaseViewSet': 'inventory',
    'StockViewSet': 'inventory',

    # Certificate
    'CertificateViewSet': 'certificate',
    'CertificateTemplateViewSet': 'certificate',

    # Online Classes
    'OnlineClassViewSet': 'online_class',
    'LiveSessionViewSet': 'online_class',
    'RecordingViewSet': 'online_class',

    # Assignment & Homework
    'AssignmentViewSet': 'assignment',
    'HomeworkViewSet': 'homework',
    'SubmissionViewSet': 'assignment',

    # Default fallback (will try to infer from ViewSet name)
    # Example: FooBarViewSet -> foo_bar
}


def get_module_name_from_viewset(viewset_name):
    """
    Extract module name from ViewSet class name
    Example: StudentViewSet -> student
    """
    # Check explicit mapping first
    if viewset_name in ACL_MODULE_MAPPING:
        return ACL_MODULE_MAPPING[viewset_name]

    # Fallback: Remove 'ViewSet' and convert to snake_case
    name = viewset_name.replace('ViewSet', '')
    # Convert CamelCase to snake_case
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    return name


def find_viewsets_in_file(file_path):
    """Find all ViewSet classes in a Python file"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Find ViewSet class definitions
    pattern = r'class\s+(\w+ViewSet)\s*\([^)]*viewsets\.(?:ModelViewSet|ReadOnlyModelViewSet|GenericViewSet)'
    matches = re.finditer(pattern, content)

    viewsets = []
    for match in matches:
        viewset_name = match.group(1)
        viewsets.append({
            'name': viewset_name,
            'start_pos': match.start(),
            'module': get_module_name_from_viewset(viewset_name)
        })

    return viewsets, content


def check_has_permission_imports(content):
    """Check if file already has permission imports"""
    has_base_permission = 'BaseModelPermission' in content
    has_audit_mixin = 'AuditLoggingMixin' in content
    has_import = 'from apps.core.permissions_enterprise import' in content

    return {
        'has_base_permission': has_base_permission,
        'has_audit_mixin': has_audit_mixin,
        'has_import': has_import
    }


def add_permission_imports(content):
    """Add permission imports to file"""
    import_line = "from apps.core.permissions_enterprise import BaseModelPermission, AuditLoggingMixin\n"

    # Find where to insert (after other imports, before class definitions)
    lines = content.split('\n')
    insert_pos = 0

    # Find last import or from statement
    for i, line in enumerate(lines):
        if line.strip().startswith(('import ', 'from ')) and 'import' in line:
            insert_pos = i + 1

    # Insert import
    lines.insert(insert_pos, import_line)
    return '\n'.join(lines)


def update_viewset_class(content, viewset_info):
    """Update a ViewSet class to include permissions and audit logging"""
    viewset_name = viewset_info['name']
    module_name = viewset_info['module']

    # Find the ViewSet class definition
    pattern = rf'(class\s+{viewset_name}\s*\()([^)]*)(viewsets\.(?:ModelViewSet|ReadOnlyModelViewSet|GenericViewSet))'
    match = re.search(pattern, content)

    if not match:
        return content, False

    # Check if already has AuditLoggingMixin
    class_def = match.group(0)
    if 'AuditLoggingMixin' in class_def:
        return content, False  # Already updated

    # Update class definition to include mixin
    old_class_def = match.group(0)
    new_class_def = f"{match.group(1)}AuditLoggingMixin, {match.group(3)}"
    content = content.replace(old_class_def, new_class_def)

    # Find class body and add permission_module and audit_resource_type
    # Find the indentation
    class_start = content.find(new_class_def)
    class_body_start = content.find(':', class_start) + 1

    # Find next line after class definition
    next_line_start = content.find('\n', class_body_start) + 1

    # Determine indentation (usually 4 spaces)
    indent = '    '

    # Check if permission_classes already exists
    permission_section = content[class_body_start:class_body_start+500]

    lines_to_add = []

    if 'permission_classes' not in permission_section:
        lines_to_add.append(f"{indent}permission_classes = [IsAuthenticated, BaseModelPermission]")
    elif 'BaseModelPermission' not in permission_section:
        # Update existing permission_classes to add BaseModelPermission
        perm_pattern = rf'({indent}permission_classes\s*=\s*\[)([^\]]*)'
        perm_match = re.search(perm_pattern, permission_section)
        if perm_match:
            old_perm = perm_match.group(0)
            # Add BaseModelPermission to existing list
            new_perm = old_perm.rstrip() + ', BaseModelPermission'
            content = content.replace(old_perm, new_perm, 1)

    if 'permission_module' not in permission_section:
        lines_to_add.append(f"{indent}permission_module = '{module_name}'")

    if 'audit_resource_type' not in permission_section:
        lines_to_add.append(f"{indent}audit_resource_type = '{module_name}'")

    if lines_to_add:
        # Insert after class definition
        insert_text = '\n' + '\n'.join(lines_to_add) + '\n'
        content = content[:next_line_start] + insert_text + content[next_line_start:]
        return content, True

    return content, False


def update_file(file_path, dry_run=True):
    """Update a single views.py file"""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Processing: {file_path}")

    viewsets, content = find_viewsets_in_file(file_path)

    if not viewsets:
        print("  No ViewSets found")
        return False

    print(f"  Found {len(viewsets)} ViewSet(s):")
    for vs in viewsets:
        print(f"    - {vs['name']} (module: {vs['module']})")

    # Check imports
    import_status = check_has_permission_imports(content)

    original_content = content
    modified = False

    # Add imports if needed
    if not import_status['has_import']:
        print("  Adding permission imports...")
        content = add_permission_imports(content)
        modified = True

    # Update each ViewSet
    for vs in viewsets:
        updated_content, was_updated = update_viewset_class(content, vs)
        if was_updated:
            print(f"  Updated {vs['name']}")
            content = updated_content
            modified = True

    if modified and not dry_run:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"  ✓ File updated successfully")
    elif modified:
        print(f"  [DRY RUN] Would update this file")
    else:
        print(f"  Already up to date")

    return modified


def find_all_views_files(base_dir, app_name=None):
    """Find all views.py files in apps"""
    views_files = []
    apps_dir = Path(base_dir) / 'apps'

    if app_name:
        # Single app
        app_dir = apps_dir / app_name
        if app_dir.exists():
            views_file = app_dir / 'views.py'
            if views_file.exists():
                views_files.append(views_file)
    else:
        # All apps
        for app_dir in apps_dir.iterdir():
            if app_dir.is_dir() and not app_dir.name.startswith('_'):
                views_file = app_dir / 'views.py'
                if views_file.exists():
                    views_files.append(views_file)

    return views_files


def main():
    parser = argparse.ArgumentParser(
        description='Bulk update ViewSets with enterprise permissions and audit logging'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying them'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply changes to files'
    )
    parser.add_argument(
        '--app',
        type=str,
        help='Update specific app only (e.g., student_management)'
    )
    parser.add_argument(
        '--base-dir',
        type=str,
        default='/home/anant/ERP-MAIN-PROJECT/backend',
        help='Base directory of the project'
    )

    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Error: Must specify either --dry-run or --apply")
        return

    dry_run = args.dry_run

    print("=" * 80)
    print("ViewSet Permission & Audit Logging Updater")
    print("=" * 80)

    if dry_run:
        print("\n⚠️  DRY RUN MODE - No files will be modified")
    else:
        print("\n✓ APPLY MODE - Files will be updated")

    # Find all views.py files
    views_files = find_all_views_files(args.base_dir, args.app)

    print(f"\nFound {len(views_files)} views.py file(s)")

    if not views_files:
        print("No views.py files found!")
        return

    # Process each file
    updated_count = 0
    for views_file in views_files:
        if update_file(views_file, dry_run=dry_run):
            updated_count += 1

    print("\n" + "=" * 80)
    print(f"Summary: {updated_count}/{len(views_files)} files {'would be ' if dry_run else ''}updated")
    print("=" * 80)

    if dry_run:
        print("\nTo apply changes, run with --apply flag")


if __name__ == '__main__':
    main()
