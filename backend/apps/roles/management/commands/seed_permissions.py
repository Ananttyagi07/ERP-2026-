"""
Django management command to seed all 37 modules with their permissions
This creates the complete ACL permission structure as per your requirements
"""
from django.core.management.base import BaseCommand
from apps.roles.models import Permission, Role


class Command(BaseCommand):
    help = 'Seed all 37 modules with their permissions (View, Add, Edit, Delete)'

    # Complete list of all 37 modules with their features
    MODULES = {
        'setting': {
            'name': 'Setting',
            'features': [
                {'name': 'General Setting', 'code': 'general_setting', 'only_admin': True},
                {'name': 'Payment Setting', 'code': 'payment_setting', 'only_admin': True},
                {'name': 'SMS Setting', 'code': 'sms_setting', 'only_admin': True},
                {'name': 'Email Setting', 'code': 'email_setting', 'only_admin': True},
                {'name': 'Global Search', 'code': 'global_search'},
                {'name': 'Global Session Change', 'code': 'global_session_change'},
                {'name': 'Opening Hour', 'code': 'opening_hour', 'only_admin': True},
            ]
        },
        'theme': {
            'name': 'Theme',
            'features': [
                {'name': 'Theme', 'code': 'theme'},
            ]
        },
        'language': {
            'name': 'Language',
            'features': [
                {'name': 'Language', 'code': 'language'},
            ]
        },
        'administrator': {
            'name': 'Administrator',
            'features': [
                {'name': 'Academic Year', 'code': 'academic_year'},
                {'name': 'User Role', 'code': 'user_role', 'only_superadmin': True},
                {'name': 'Role Permission', 'code': 'role_permission', 'only_superadmin': True},
                {'name': 'Manage User', 'code': 'manage_user'},
                {'name': 'Reset User Password', 'code': 'reset_user_password'},
                {'name': 'Backup Database', 'code': 'backup_database', 'only_superadmin': True},
                {'name': 'School', 'code': 'school', 'only_superadmin': True},
                {'name': 'Payment', 'code': 'payment_gateway', 'only_superadmin': True},
                {'name': 'SMS', 'code': 'sms_gateway', 'only_superadmin': True},
                {'name': 'SMS Template', 'code': 'sms_template'},
                {'name': 'Email Template', 'code': 'email_template'},
                {'name': 'Activity Log', 'code': 'activity_log'},
                {'name': 'Super Admin', 'code': 'super_admin', 'only_superadmin': True},
                {'name': 'Guardian Feedback', 'code': 'guardian_feedback'},
                {'name': 'User Credential', 'code': 'user_credential'},
                {'name': 'Username', 'code': 'username'},
            ]
        },
        'human_resource': {
            'name': 'Human Resource',
            'features': [
                {'name': 'Designation', 'code': 'designation'},
                {'name': 'Employee', 'code': 'employee'},
            ]
        },
        'teacher': {
            'name': 'Teacher',
            'features': [
                {'name': 'Teacher', 'code': 'teacher'},
                {'name': 'Teacher Lecture', 'code': 'teacher_lecture'},
                {'name': 'Department', 'code': 'department'},
                {'name': 'Rating', 'code': 'rating'},
            ]
        },
        'academic_activity': {
            'name': 'Academic Activity',
            'features': [
                {'name': 'Classes', 'code': 'classes'},
                {'name': 'Section', 'code': 'section'},
                {'name': 'Subject', 'code': 'subject'},
                {'name': 'Syllabus', 'code': 'syllabus'},
                {'name': 'Class Routine', 'code': 'class_routine'},
                {'name': 'Promotion', 'code': 'promotion'},
                {'name': 'Material', 'code': 'material'},
                {'name': 'Live Class', 'code': 'live_class'},
                {'name': 'Assignment', 'code': 'assignment'},
                {'name': 'Submission', 'code': 'submission'},
            ]
        },
        'guardian': {
            'name': 'Guardian',
            'features': [
                {'name': 'Guardian', 'code': 'guardian'},
                {'name': 'Feedback', 'code': 'feedback'},
            ]
        },
        'student': {
            'name': 'Student',
            'features': [
                {'name': 'Student', 'code': 'student'},
                {'name': 'Bulk Import', 'code': 'bulk_import'},
                {'name': 'Student Activity', 'code': 'student_activity'},
                {'name': 'Online Admission', 'code': 'online_admission'},
                {'name': 'Student Type', 'code': 'student_type'},
            ]
        },
        'attendance': {
            'name': 'Attendance',
            'features': [
                {'name': 'Employee Attendance', 'code': 'employee_attendance'},
                {'name': 'Teacher Attendance', 'code': 'teacher_attendance'},
                {'name': 'Student Attendance', 'code': 'student_attendance'},
                {'name': 'Absent Email', 'code': 'absent_email'},
                {'name': 'Absent SMS', 'code': 'absent_sms'},
            ]
        },
        'exam': {
            'name': 'Exam',
            'features': [
                {'name': 'Exam Term', 'code': 'exam_term'},
                {'name': 'Exam Grade', 'code': 'exam_grade'},
                {'name': 'Exam Schedule', 'code': 'exam_schedule'},
                {'name': 'Exam Suggestion', 'code': 'exam_suggestion'},
                {'name': 'Exam Attendance', 'code': 'exam_attendance'},
            ]
        },
        'exam_mark': {
            'name': 'Exam Mark',
            'features': [
                {'name': 'Exam Mark', 'code': 'exam_mark'},
                {'name': 'Mark Sheet', 'code': 'mark_sheet'},
                {'name': 'Result', 'code': 'result'},
                {'name': 'Mark send by SMS', 'code': 'mark_sms'},
                {'name': 'Mark send by Email', 'code': 'mark_email'},
                {'name': 'Exam Result', 'code': 'exam_result'},
                {'name': 'Final Result', 'code': 'final_result'},
                {'name': 'Merit List', 'code': 'merit_list'},
                {'name': 'Result Email', 'code': 'result_email'},
                {'name': 'Result SMS', 'code': 'result_sms'},
                {'name': 'Result Card', 'code': 'result_card'},
            ]
        },
        'library': {
            'name': 'Library',
            'features': [
                {'name': 'Library Book', 'code': 'library_book'},
                {'name': 'Library Member', 'code': 'library_member'},
                {'name': 'Issue & Return', 'code': 'issue_return'},
                {'name': 'e-book', 'code': 'ebook'},
            ]
        },
        'transport': {
            'name': 'Transport',
            'features': [
                {'name': 'Vehicle', 'code': 'vehicle'},
                {'name': 'Transport Route', 'code': 'transport_route'},
                {'name': 'Transport Member', 'code': 'transport_member'},
            ]
        },
        'hostel': {
            'name': 'Hostel',
            'features': [
                {'name': 'Hostel', 'code': 'hostel'},
                {'name': 'Hostel Room', 'code': 'hostel_room'},
                {'name': 'Hostel Member', 'code': 'hostel_member'},
            ]
        },
        'messaging': {
            'name': 'Message, Email & SMS',
            'features': [
                {'name': 'Email', 'code': 'email'},
                {'name': 'Text SMS', 'code': 'text_sms'},
                {'name': 'Message', 'code': 'message'},
            ]
        },
        'announcement': {
            'name': 'Announcement',
            'features': [
                {'name': 'Notice', 'code': 'notice'},
                {'name': 'News', 'code': 'news'},
                {'name': 'Holiday', 'code': 'holiday'},
            ]
        },
        'event': {
            'name': 'Event',
            'features': [
                {'name': 'Event', 'code': 'event'},
            ]
        },
        'front_office': {
            'name': 'Front Office',
            'features': [
                {'name': 'Visitor', 'code': 'visitor'},
                {'name': 'Visitor Purpose', 'code': 'visitor_purpose'},
                {'name': 'Call Logs', 'code': 'call_logs'},
                {'name': 'Postal Dispatch', 'code': 'postal_dispatch'},
                {'name': 'Postal Receive', 'code': 'postal_receive'},
                {'name': 'Front Office', 'code': 'front_office'},
            ]
        },
        'accounting': {
            'name': 'Accounting',
            'features': [
                {'name': 'Expenditure Head', 'code': 'expenditure_head'},
                {'name': 'Expenditure', 'code': 'expenditure'},
                {'name': 'Income Head', 'code': 'income_head'},
                {'name': 'Income', 'code': 'income'},
                {'name': 'Invoice', 'code': 'invoice'},
                {'name': 'Payment', 'code': 'payment'},
                {'name': 'Discount', 'code': 'discount'},
                {'name': 'Fee Type', 'code': 'fee_type'},
                {'name': 'Due Fee Email', 'code': 'due_fee_email'},
                {'name': 'Due Fee SMS', 'code': 'due_fee_sms'},
                {'name': 'Invoice Receipt', 'code': 'invoice_receipt'},
            ]
        },
        'report': {
            'name': 'Report',
            'features': [
                {'name': 'Report', 'code': 'report'},
            ]
        },
        'certificate': {
            'name': 'Certificate',
            'features': [
                {'name': 'Certificate Type', 'code': 'certificate_type'},
                {'name': 'Certificate', 'code': 'certificate'},
            ]
        },
        'media_gallery': {
            'name': 'Media Gallery',
            'features': [
                {'name': 'Gallery', 'code': 'gallery'},
                {'name': 'Image', 'code': 'image'},
            ]
        },
        'frontend': {
            'name': 'Frontend',
            'features': [
                {'name': 'Frontend', 'code': 'frontend'},
                {'name': 'Home Slider', 'code': 'home_slider'},
                {'name': 'About', 'code': 'about'},
            ]
        },
        'payroll': {
            'name': 'Payroll',
            'features': [
                {'name': 'Salary Grade', 'code': 'salary_grade'},
                {'name': 'Payment', 'code': 'payroll_payment'},
                {'name': 'History', 'code': 'payroll_history'},
            ]
        },
        'complain': {
            'name': 'Complain',
            'features': [
                {'name': 'Complain', 'code': 'complain'},
                {'name': 'Complain Type', 'code': 'complain_type'},
            ]
        },
        'user_complain': {
            'name': 'User Complain',
            'features': [
                {'name': 'User Complain', 'code': 'user_complain', 'except_superadmin': True},
            ]
        },
        'user_leave': {
            'name': 'User Leave',
            'features': [
                {'name': 'User Leave', 'code': 'user_leave', 'except_superadmin': True},
            ]
        },
        'leave_management': {
            'name': 'Leave Management',
            'features': [
                {'name': 'Leave Management', 'code': 'leave_management'},
                {'name': 'Leave Type', 'code': 'leave_type'},
                {'name': 'Leave Application', 'code': 'leave_application'},
                {'name': 'Waiting Leave', 'code': 'waiting_leave'},
                {'name': 'Approve Leave', 'code': 'approve_leave'},
                {'name': 'Decline Leave', 'code': 'decline_leave'},
            ]
        },
        'id_card': {
            'name': 'ID Card & Admit Card',
            'features': [
                {'name': 'ID & Admit card', 'code': 'id_admit_card'},
                {'name': 'Teacher ID card', 'code': 'teacher_id_card'},
                {'name': 'Employee ID Card', 'code': 'employee_id_card'},
                {'name': 'Student ID card', 'code': 'student_id_card'},
                {'name': 'ID Card Setting', 'code': 'id_card_setting', 'only_superadmin': True},
                {'name': 'Admit Card Setting', 'code': 'admit_card_setting', 'only_superadmin': True},
                {'name': 'Admit card', 'code': 'admit_card'},
                {'name': 'School ID Setting', 'code': 'school_id_setting', 'only_admin': True},
                {'name': 'School Admit Setting', 'code': 'school_admit_setting', 'only_admin': True},
            ]
        },
        'miscellaneous': {
            'name': 'Miscellaneous',
            'features': [
                {'name': 'Award', 'code': 'award'},
                {'name': 'Faq', 'code': 'faq'},
                {'name': 'Todo', 'code': 'todo'},
            ]
        },
        'scholarship': {
            'name': 'Scholarship',
            'features': [
                {'name': 'Candidate', 'code': 'candidate'},
                {'name': 'Donar', 'code': 'donar'},
                {'name': 'Scholarship', 'code': 'scholarship'},
            ]
        },
        'asset_management': {
            'name': 'Asset Management',
            'features': [
                {'name': 'Category', 'code': 'asset_category'},
                {'name': 'Issue', 'code': 'asset_issue'},
                {'name': 'Item Category', 'code': 'asset_item_category'},
                {'name': 'Purchase', 'code': 'asset_purchase'},
                {'name': 'Store', 'code': 'store'},
                {'name': 'Vendor', 'code': 'vendor'},
            ]
        },
        'inventory': {
            'name': 'Inventory',
            'features': [
                {'name': 'Item Category', 'code': 'item_category'},
                {'name': 'Item Supplier', 'code': 'item_supplier'},
                {'name': 'Item Warehouse', 'code': 'item_warehouse'},
                {'name': 'Item Product', 'code': 'item_product'},
                {'name': 'Item Purchase', 'code': 'item_purchase'},
                {'name': 'Item Sale', 'code': 'item_sale'},
                {'name': 'Item Issue', 'code': 'item_issue'},
            ]
        },
        'lessonplan': {
            'name': 'Lessonplan',
            'features': [
                {'name': 'Lessonplan', 'code': 'lessonplan'},
                {'name': 'Lesson', 'code': 'lesson'},
                {'name': 'Topic', 'code': 'topic'},
                {'name': 'Status', 'code': 'lessonplan_status'},
                {'name': 'Timeline', 'code': 'timeline'},
            ]
        },
        'online_exam': {
            'name': 'Online Exam',
            'features': [
                {'name': 'Take Exam', 'code': 'take_exam'},
                {'name': 'Online Exam', 'code': 'online_exam'},
                {'name': 'Question Bank', 'code': 'question_bank'},
                {'name': 'Exam Instructions', 'code': 'exam_instructions'},
            ]
        },
        'subscription': {
            'name': 'Subscription',
            'features': [
                {'name': 'Faqs', 'code': 'subscription_faqs', 'only_superadmin': True},
                {'name': 'Slider', 'code': 'subscription_slider', 'only_superadmin': True},
                {'name': 'Subscription', 'code': 'subscription', 'only_superadmin': True},
                {'name': 'Setting', 'code': 'subscription_setting', 'only_superadmin': True},
                {'name': 'Plan', 'code': 'subscription_plan', 'only_superadmin': True},
            ]
        },
    }

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed permissions...'))

        # Permission actions
        actions = ['view', 'add', 'edit', 'delete']

        created_count = 0
        existing_count = 0

        # Iterate through all modules
        for module_code, module_data in self.MODULES.items():
            module_name = module_data['name']

            for feature in module_data['features']:
                feature_name = feature['name']
                feature_code = feature['code']

                # Create permissions for each action
                for action in actions:
                    permission_codename = f"{action}_{feature_code}"
                    permission_name = f"{action.title()} {feature_name}"

                    # Add restrictions to description if any
                    description_parts = [f"{action.title()} permission for {feature_name}"]

                    if feature.get('only_superadmin'):
                        description_parts.append("(Only Super Admin)")
                    elif feature.get('only_admin'):
                        description_parts.append("(Only Admin)")
                    elif feature.get('except_superadmin'):
                        description_parts.append("(Except Super Admin)")

                    description = " ".join(description_parts)

                    # Create or get permission
                    permission, created = Permission.objects.get_or_create(
                        codename=permission_codename,
                        defaults={
                            'name': permission_name,
                            'module': module_code,
                            'description': description
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Created: {permission_codename}')
                        )
                    else:
                        existing_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Seeding complete! Created {created_count} new permissions, '
                f'{existing_count} already existed.'
            )
        )

        # Create default roles if they don't exist
        self.create_default_roles()

    def create_default_roles(self):
        """Create the 5 default system roles"""
        self.stdout.write('\nCreating default roles...')

        default_roles = [
            {
                'name': 'Superadmin',
                'description': 'Full ERP control - Development team',
                'is_system_role': True,
                'is_default': True
            },
            {
                'name': 'Admin',
                'description': 'College-level management',
                'is_system_role': True,
                'is_default': True
            },
            {
                'name': 'Teacher',
                'description': 'Teaching and course management',
                'is_system_role': True,
                'is_default': True
            },
            {
                'name': 'Student',
                'description': 'Student portal access',
                'is_system_role': True,
                'is_default': True
            },
            {
                'name': 'Staff',
                'description': 'Support staff functions',
                'is_system_role': True,
                'is_default': True
            },
        ]

        for role_data in default_roles:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults=role_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created role: {role.name}')
                )

        self.stdout.write(self.style.SUCCESS('\n✓ Default roles created!'))
