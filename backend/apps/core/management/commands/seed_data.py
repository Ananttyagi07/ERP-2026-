from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from apps.colleges.models import College, Department
from apps.accounting.models import Payment, Invoice
from apps.announcement.models import Notice
from apps.event.models import Event
from apps.teachers.models import Teacher
from apps.students.models import Student
from apps.academic.models import SchoolClass, ClassSection, Subject
from apps.users.models import User
from apps.hr.models import Designation, Employee


class Command(BaseCommand):
    help = 'Seed database with comprehensive test data for both colleges including students, teachers, and staff'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('Starting comprehensive data seeding...'))
        self.stdout.write(self.style.SUCCESS('='*70))

        try:
            # Get the two colleges
            college_eng = College.objects.get(id=1)  # School of Engineering
            college_arts = College.objects.get(id=2)  # School of Arts

            # Seed data for each college
            self.seed_college_data(college_eng, 'Engineering')
            self.seed_college_data(college_arts, 'Arts')

            self.stdout.write(self.style.SUCCESS('\n' + '='*70))
            self.stdout.write(self.style.SUCCESS('✓ Data seeding completed successfully!'))
            self.stdout.write(self.style.SUCCESS('='*70 + '\n'))
        except College.DoesNotExist:
            self.stdout.write(self.style.ERROR('Error: Required colleges not found. Please create colleges with IDs 1 and 2 first.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during seeding: {str(e)}'))
            import traceback
            traceback.print_exc()

    def seed_college_data(self, college, college_type):
        """Seed comprehensive data for a specific college"""
        self.stdout.write(f'\n{"="*70}')
        self.stdout.write(f'Seeding data for {college.name} ({college_type})')
        self.stdout.write(f'{"="*70}')

        # Create academic structures first
        self._create_academic_structure(college, college_type)

        # Create departments (skip if there are DB migration issues)
        try:
            self._create_departments(college, college_type)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  ⚠ Skipping departments due to database schema issue'))

        # Create designations
        self._create_designations(college, college_type)

        # Create teachers
        self._create_teachers(college, college_type)

        # Create students
        self._create_students(college, college_type)

        # Create staff members
        self._create_staff(college, college_type)

        # Create announcements
        self._create_announcements(college, college_type)

        # Create events
        self._create_events(college, college_type)

        # Create payments (skip if DB schema issues)
        try:
            self._create_payments(college, college_type)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  ⚠ Skipping payments due to database schema issue: invoice_id constraint'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Completed seeding for {college.name}'))

    def _create_academic_structure(self, college, college_type):
        """Create class and section structure"""
        self.stdout.write('\n📚 Creating academic structure...')

        if college_type == 'Engineering':
            classes_data = [
                {'name': 'First Year (FY)', 'numeric_name': 1},
                {'name': 'Second Year (SY)', 'numeric_name': 2},
                {'name': 'Third Year (TY)', 'numeric_name': 3},
                {'name': 'Final Year (FY Final)', 'numeric_name': 4},
            ]
        else:  # Arts
            classes_data = [
                {'name': 'First Year (FY)', 'numeric_name': 1},
                {'name': 'Second Year (SY)', 'numeric_name': 2},
                {'name': 'Third Year (TY)', 'numeric_name': 3},
            ]

        for class_data in classes_data:
            school_class, created = SchoolClass.objects.get_or_create(
                college=college,
                name=class_data['name'],
                defaults={'numeric_name': class_data['numeric_name']}
            )

            # Create sections for each class
            for section_name in ['A', 'B', 'C']:
                ClassSection.objects.get_or_create(
                    school_class=school_class,
                    name=section_name,
                    defaults={'college': college}
                )

        self.stdout.write(f'  ✓ Created academic structure with classes and sections')

    def _create_departments(self, college, college_type):
        """Create departments"""
        self.stdout.write('\n🏢 Creating departments...')

        if college_type == 'Engineering':
            departments_data = [
                {'name': 'Computer Science', 'code': 'CSE'},
                {'name': 'Mechanical Engineering', 'code': 'ME'},
                {'name': 'Electrical Engineering', 'code': 'EE'},
                {'name': 'Electronics Engineering', 'code': 'EC'},
            ]
        else:  # Arts
            departments_data = [
                {'name': 'English Literature', 'code': 'ENG'},
                {'name': 'History', 'code': 'HIST'},
                {'name': 'Political Science', 'code': 'PS'},
                {'name': 'Philosophy', 'code': 'PHIL'},
            ]

        count = 0
        for dept_data in departments_data:
            Department.objects.get_or_create(
                college=college,
                name=dept_data['name'],
                defaults={'code': dept_data['code']}
            )
            count += 1

        self.stdout.write(f'  ✓ Created {count} departments')

    def _create_designations(self, college, college_type):
        """Create job designations"""
        self.stdout.write('\n👔 Creating designations...')

        designations_data = [
            {'name': 'Principal', 'description': 'Head of the college'},
            {'name': 'Vice Principal', 'description': 'Deputy head of the college'},
            {'name': 'Professor', 'description': 'Senior academic staff'},
            {'name': 'Associate Professor', 'description': 'Mid-level academic staff'},
            {'name': 'Assistant Professor', 'description': 'Junior academic staff'},
            {'name': 'Office Manager', 'description': 'Administrative staff'},
            {'name': 'Account Manager', 'description': 'Finance staff'},
            {'name': 'Support Staff', 'description': 'General support personnel'},
        ]

        count = 0
        for desig_data in designations_data:
            Designation.objects.get_or_create(
                college=college,
                name=desig_data['name'],
                defaults={'description': desig_data['description']}
            )
            count += 1

        self.stdout.write(f'  ✓ Created {count} designations')

    def _create_teachers(self, college, college_type):
        """Create 15+ teachers"""
        self.stdout.write('\n👨‍🏫 Creating teachers...')

        if college_type == 'Engineering':
            teachers_data = [
                {'name': 'Dr. Rajesh Kumar', 'email': 'rajesh.kumar@eng.edu'},
                {'name': 'Prof. Ananya Sharma', 'email': 'ananya.sharma@eng.edu'},
                {'name': 'Dr. Vikram Singh', 'email': 'vikram.singh@eng.edu'},
                {'name': 'Prof. Priya Patel', 'email': 'priya.patel@eng.edu'},
                {'name': 'Dr. Arjun Gupta', 'email': 'arjun.gupta@eng.edu'},
                {'name': 'Prof. Neha Mishra', 'email': 'neha.mishra@eng.edu'},
                {'name': 'Dr. Sanjay Verma', 'email': 'sanjay.verma@eng.edu'},
                {'name': 'Prof. Divya Nair', 'email': 'divya.nair@eng.edu'},
                {'name': 'Dr. Arun Chopra', 'email': 'arun.chopra@eng.edu'},
                {'name': 'Prof. Shreya Bansal', 'email': 'shreya.bansal@eng.edu'},
                {'name': 'Dr. Manoj Yadav', 'email': 'manoj.yadav@eng.edu'},
                {'name': 'Prof. Deepika Roy', 'email': 'deepika.roy@eng.edu'},
                {'name': 'Dr. Suresh Tiwari', 'email': 'suresh.tiwari@eng.edu'},
                {'name': 'Prof. Kavya Joshi', 'email': 'kavya.joshi@eng.edu'},
                {'name': 'Dr. Ramesh Bhat', 'email': 'ramesh.bhat@eng.edu'},
                {'name': 'Prof. Anita Desai', 'email': 'anita.desai@eng.edu'},
                {'name': 'Dr. Akshay Saxena', 'email': 'akshay.saxena@eng.edu'},
            ]
        else:  # Arts
            teachers_data = [
                {'name': 'Dr. Amrita Sengupta', 'email': 'amrita.sengupta@arts.edu'},
                {'name': 'Prof. Samrat Mukherjee', 'email': 'samrat.mukherjee@arts.edu'},
                {'name': 'Dr. Ritika Banerjee', 'email': 'ritika.banerjee@arts.edu'},
                {'name': 'Prof. Sourav Das', 'email': 'sourav.das@arts.edu'},
                {'name': 'Dr. Priyanka Chatterjee', 'email': 'priyanka.chatterjee@arts.edu'},
                {'name': 'Prof. Rohit Dutta', 'email': 'rohit.dutta@arts.edu'},
                {'name': 'Dr. Sanjana Mehta', 'email': 'sanjana.mehta@arts.edu'},
                {'name': 'Prof. Vikram Reddy', 'email': 'vikram.reddy@arts.edu'},
                {'name': 'Dr. Anjali Singh', 'email': 'anjali.singh@arts.edu'},
                {'name': 'Prof. Karan Malhotra', 'email': 'karan.malhotra@arts.edu'},
                {'name': 'Dr. Nisha Pandey', 'email': 'nisha.pandey@arts.edu'},
                {'name': 'Prof. Aditya Kumar', 'email': 'aditya.kumar@arts.edu'},
                {'name': 'Dr. Ravi Sharma', 'email': 'ravi.sharma@arts.edu'},
                {'name': 'Prof. Meera Nair', 'email': 'meera.nair@arts.edu'},
                {'name': 'Dr. Sanjay Iyer', 'email': 'sanjay.iyer@arts.edu'},
                {'name': 'Prof. Leela Krishnan', 'email': 'leela.krishnan@arts.edu'},
                {'name': 'Dr. Abhishek Verma', 'email': 'abhishek.verma@arts.edu'},
            ]

        try:
            departments = list(Department.objects.filter(college=college))
        except:
            departments = []

        designation = Designation.objects.filter(college=college, name='Assistant Professor').first()

        if not designation:
            designation = Designation.objects.filter(college=college).first()

        count = 0
        for idx, teacher_data in enumerate(teachers_data):
            try:
                # Create user for teacher
                user, _ = User.objects.get_or_create(
                    email=teacher_data['email'],
                    defaults={
                        'username': teacher_data['email'].split('@')[0],
                        'first_name': teacher_data['name'].split()[0],
                        'last_name': ' '.join(teacher_data['name'].split()[1:]),
                        'is_active': True,
                    }
                )
                user.set_password('teacher123')
                user.save()

                # Create teacher profile (department is optional)
                if not Teacher.objects.filter(user=user).exists():
                    Teacher.objects.create(
                        user=user,
                        college=college,
                        department=departments[idx % len(departments)] if departments else None,
                        designation=designation,
                        national_id=f'TEACH{college.id}{idx+1:04d}',
                        joining_date=(timezone.now() - timedelta(days=365*2)).date(),
                        qualification='M.Tech / M.A.',
                        experience_years=5 + (idx % 10),
                    )
                    count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠ Could not create teacher {teacher_data["name"]}: {str(e)}'))

        self.stdout.write(f'  ✓ Created {count} teachers')

    def _create_students(self, college, college_type):
        """Create 15+ students"""
        self.stdout.write('\n👨‍🎓 Creating students...')

        if college_type == 'Engineering':
            students_data = [
                {'name': 'Akshay Sharma', 'email': 'akshay.sharma@student.eng.edu'},
                {'name': 'Bhavna Gupta', 'email': 'bhavna.gupta@student.eng.edu'},
                {'name': 'Chetan Verma', 'email': 'chetan.verma@student.eng.edu'},
                {'name': 'Divya Sinha', 'email': 'divya.sinha@student.eng.edu'},
                {'name': 'Eshan Kumar', 'email': 'eshan.kumar@student.eng.edu'},
                {'name': 'Fiona Joshi', 'email': 'fiona.joshi@student.eng.edu'},
                {'name': 'Gaurav Yadav', 'email': 'gaurav.yadav@student.eng.edu'},
                {'name': 'Harshit Nair', 'email': 'harshit.nair@student.eng.edu'},
                {'name': 'Ishita Desai', 'email': 'ishita.desai@student.eng.edu'},
                {'name': 'Jaideep Singh', 'email': 'jaideep.singh@student.eng.edu'},
                {'name': 'Kriti Patel', 'email': 'kriti.patel@student.eng.edu'},
                {'name': 'Lakshay Saxena', 'email': 'lakshay.saxena@student.eng.edu'},
                {'name': 'Megha Trivedi', 'email': 'megha.trivedi@student.eng.edu'},
                {'name': 'Nikhil Bhat', 'email': 'nikhil.bhat@student.eng.edu'},
                {'name': 'Oma Chandra', 'email': 'oma.chandra@student.eng.edu'},
                {'name': 'Payal Reddy', 'email': 'payal.reddy@student.eng.edu'},
                {'name': 'Quentin Dias', 'email': 'quentin.dias@student.eng.edu'},
            ]
        else:  # Arts
            students_data = [
                {'name': 'Ramesh Kumar', 'email': 'ramesh.kumar@student.arts.edu'},
                {'name': 'Shalini Kapoor', 'email': 'shalini.kapoor@student.arts.edu'},
                {'name': 'Tarun Malhotra', 'email': 'tarun.malhotra@student.arts.edu'},
                {'name': 'Uma Sharma', 'email': 'uma.sharma@student.arts.edu'},
                {'name': 'Varun Iyer', 'email': 'varun.iyer@student.arts.edu'},
                {'name': 'Winnie Fernandes', 'email': 'winnie.fernandes@student.arts.edu'},
                {'name': 'Xander Lewis', 'email': 'xander.lewis@student.arts.edu'},
                {'name': 'Yara Agarwal', 'email': 'yara.agarwal@student.arts.edu'},
                {'name': 'Zainab Khan', 'email': 'zainab.khan@student.arts.edu'},
                {'name': 'Aditya Patel', 'email': 'aditya.patel@student.arts.edu'},
                {'name': 'Bhakti Singh', 'email': 'bhakti.singh@student.arts.edu'},
                {'name': 'Chirag Mishra', 'email': 'chirag.mishra@student.arts.edu'},
                {'name': 'Diya Bansal', 'email': 'diya.bansal@student.arts.edu'},
                {'name': 'Eshaan Kapadia', 'email': 'eshaan.kapadia@student.arts.edu'},
                {'name': 'Fayad Hussain', 'email': 'fayad.hussain@student.arts.edu'},
                {'name': 'Gitanjali Mehta', 'email': 'gitanjali.mehta@student.arts.edu'},
                {'name': 'Harsh Dutta', 'email': 'harsh.dutta@student.arts.edu'},
            ]

        classes = list(SchoolClass.objects.filter(college=college))

        count = 0
        for idx, student_data in enumerate(students_data):
            try:
                # Create user for student
                user, _ = User.objects.get_or_create(
                    email=student_data['email'],
                    defaults={
                        'username': student_data['email'].split('@')[0],
                        'first_name': student_data['name'].split()[0],
                        'last_name': ' '.join(student_data['name'].split()[1:]),
                        'is_active': True,
                    }
                )
                user.set_password('student123')
                user.save()

                # Get class and section
                school_class = classes[idx % len(classes)] if classes else None
                section = school_class.sections.first() if school_class else None

                # Create student profile
                if not Student.objects.filter(user=user).exists() and school_class and section:
                    Student.objects.create(
                        user=user,
                        college=college,
                        school_class=school_class,
                        section=section,
                        roll_number=f'{college.id}{school_class.numeric_name}{idx+1:03d}',
                        registration_number=f'REG{college.id}{school_class.numeric_name}{idx+1:04d}',
                        admission_date=(timezone.now() - timedelta(days=365*2)).date(),
                        national_id=f'STU{college.id}{idx+1:05d}',
                    )
                    count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠ Could not create student {student_data["name"]}: {str(e)}'))

        self.stdout.write(f'  ✓ Created {count} students')

    def _create_staff(self, college, college_type):
        """Create staff members"""
        self.stdout.write('\n👔 Creating staff members...')

        if college_type == 'Engineering':
            staff_data = [
                {'name': 'Rajesh Patel', 'email': 'rajesh.patel@eng.staff.edu', 'designation': 'Office Manager'},
                {'name': 'Priya Singh', 'email': 'priya.singh@eng.staff.edu', 'designation': 'Account Manager'},
                {'name': 'Vikas Kumar', 'email': 'vikas.kumar@eng.staff.edu', 'designation': 'Support Staff'},
                {'name': 'Sunita Sharma', 'email': 'sunita.sharma@eng.staff.edu', 'designation': 'Support Staff'},
                {'name': 'Deepak Verma', 'email': 'deepak.verma@eng.staff.edu', 'designation': 'Support Staff'},
            ]
        else:  # Arts
            staff_data = [
                {'name': 'Mohan Iyer', 'email': 'mohan.iyer@arts.staff.edu', 'designation': 'Office Manager'},
                {'name': 'Kavya Nair', 'email': 'kavya.nair@arts.staff.edu', 'designation': 'Account Manager'},
                {'name': 'Sanjay Reddy', 'email': 'sanjay.reddy@arts.staff.edu', 'designation': 'Support Staff'},
                {'name': 'Anita Sharma', 'email': 'anita.sharma@arts.staff.edu', 'designation': 'Support Staff'},
                {'name': 'Ravi Kumar', 'email': 'ravi.kumar@arts.staff.edu', 'designation': 'Support Staff'},
            ]

        count = 0
        for idx, staff_member in enumerate(staff_data):
            try:
                # Create user for staff
                user, _ = User.objects.get_or_create(
                    email=staff_member['email'],
                    defaults={
                        'username': staff_member['email'].split('@')[0],
                        'first_name': staff_member['name'].split()[0],
                        'last_name': ' '.join(staff_member['name'].split()[1:]),
                        'is_active': True,
                    }
                )
                user.set_password('staff123')
                user.save()

                # Get designation
                designation = Designation.objects.filter(
                    college=college,
                    name=staff_member['designation']
                ).first()

                if not designation:
                    designation = Designation.objects.filter(college=college).first()

                # Create employee profile
                if not Employee.objects.filter(user=user).exists() and designation:
                    Employee.objects.create(
                        user=user,
                        college=college,
                        designation=designation,
                        national_id=f'STAFF{college.id}{idx+1:04d}',
                        joining_date=(timezone.now() - timedelta(days=365*3)).date(),
                        qualification='12th / Diploma',
                        experience_years=3 + (idx % 5),
                    )
                    count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠ Could not create staff {staff_member["name"]}: {str(e)}'))

        self.stdout.write(f'  ✓ Created {count} staff members')

    def _create_announcements(self, college, college_type):
        """Create test announcements"""
        self.stdout.write('\n📢 Creating announcements...')

        if college_type == 'Engineering':
            announcements_data = [
                {'title': 'New Lab Equipment Installed', 'notice_text': 'Advanced robotics lab is now operational for all engineering students'},
                {'title': 'Internship Opportunities', 'notice_text': 'Multiple internship positions available at tech companies'},
                {'title': 'Course Registration Extended', 'notice_text': 'Course registration deadline extended to next Friday'},
                {'title': 'Campus Festival Announcement', 'notice_text': 'Annual engineering expo scheduled for next month'},
                {'title': 'Library Hours', 'notice_text': 'Engineering section now open on weekends'},
            ]
        else:  # Arts
            announcements_data = [
                {'title': 'New Faculty Appointments', 'notice_text': 'Meet our new professors in Literature and History departments'},
                {'title': 'Research Grant Opportunities', 'notice_text': 'Apply for government research grants for arts and humanities projects'},
                {'title': 'Cultural Week Begins', 'notice_text': 'Join us for a week celebrating diverse cultures and traditions'},
                {'title': 'Seminar Series Starts', 'notice_text': 'Weekly seminars featuring renowned scholars in the field'},
                {'title': 'Art Exhibition', 'notice_text': 'Student artwork showcase at main campus gallery'},
            ]

        count = 0
        for idx, data in enumerate(announcements_data):
            Notice.objects.get_or_create(
                college=college,
                title=data['title'],
                defaults={
                    'notice_text': data['notice_text'],
                    'date': (timezone.now() - timedelta(days=idx)).date(),
                    'notice_for': 'All',
                    'is_view_on_web': True
                }
            )
            count += 1

        self.stdout.write(f'  ✓ Created {count} announcements')

    def _create_events(self, college, college_type):
        """Create test events"""
        self.stdout.write('\n📅 Creating events...')

        if college_type == 'Engineering':
            events_data = [
                {'title': 'Annual Tech Hackathon', 'event_place': 'Engineering Building Auditorium', 'event_for': 'Students'},
                {'title': 'Robotics Competition', 'event_place': 'Engineering Lab Complex', 'event_for': 'Students'},
                {'title': 'Industry Guest Lecture', 'event_place': 'Main Hall', 'event_for': 'All'},
                {'title': 'Product Design Showcase', 'event_place': 'Innovation Center', 'event_for': 'Students'},
                {'title': 'Engineering Seminar Series', 'event_place': 'Conference Room A', 'event_for': 'Faculty'},
            ]
        else:  # Arts
            events_data = [
                {'title': 'Literature Festival', 'event_place': 'Central Auditorium', 'event_for': 'Students'},
                {'title': 'Historical Symposium', 'event_place': 'Main Conference Hall', 'event_for': 'All'},
                {'title': 'Art Exhibition Opening', 'event_place': 'Campus Gallery', 'event_for': 'Students'},
                {'title': 'Philosophy Debate', 'event_place': 'Seminar Hall', 'event_for': 'Students'},
                {'title': 'Cultural Music Night', 'event_place': 'Open Air Amphitheater', 'event_for': 'All'},
            ]

        count = 0
        for idx, data in enumerate(events_data):
            from_date = (timezone.now() + timedelta(days=30+idx)).date()
            to_date = (timezone.now() + timedelta(days=31+idx)).date()

            Event.objects.get_or_create(
                college=college,
                title=data['title'],
                defaults={
                    'event_place': data['event_place'],
                    'event_for': data['event_for'],
                    'from_date': from_date,
                    'to_date': to_date,
                    'is_view_on_web': True
                }
            )
            count += 1

        self.stdout.write(f'  ✓ Created {count} events')

    def _create_payments(self, college, college_type):
        """Create test payment data"""
        self.stdout.write('\n💰 Creating payments...')

        if college_type == 'Engineering':
            payments_data = [
                {'reference': 'ENG-PAY-001', 'amount': 15000, 'method': 'bank_transfer'},
                {'reference': 'ENG-PAY-002', 'amount': 12000, 'method': 'credit_card'},
                {'reference': 'ENG-PAY-003', 'amount': 18500, 'method': 'cash'},
                {'reference': 'ENG-PAY-004', 'amount': 9000, 'method': 'check'},
                {'reference': 'ENG-PAY-005', 'amount': 22000, 'method': 'bank_transfer'},
                {'reference': 'ENG-PAY-006', 'amount': 16500, 'method': 'credit_card'},
                {'reference': 'ENG-PAY-007', 'amount': 21000, 'method': 'cash'},
            ]
        else:  # Arts
            payments_data = [
                {'reference': 'ARTS-PAY-001', 'amount': 8000, 'method': 'bank_transfer'},
                {'reference': 'ARTS-PAY-002', 'amount': 10000, 'method': 'credit_card'},
                {'reference': 'ARTS-PAY-003', 'amount': 6500, 'method': 'cash'},
                {'reference': 'ARTS-PAY-004', 'amount': 11000, 'method': 'bank_transfer'},
                {'reference': 'ARTS-PAY-005', 'amount': 7500, 'method': 'check'},
                {'reference': 'ARTS-PAY-006', 'amount': 9500, 'method': 'credit_card'},
                {'reference': 'ARTS-PAY-007', 'amount': 8500, 'method': 'cash'},
            ]

        count = 0
        for idx, data in enumerate(payments_data):
            Payment.objects.get_or_create(
                college=college,
                reference=data['reference'],
                defaults={
                    'amount': data['amount'],
                    'payment_date': (timezone.now() - timedelta(days=idx)).date(),
                    'payment_method': data['method'],
                    'note': f"Payment for {college.name} - Reference: {data['reference']}"
                }
            )
            count += 1

        self.stdout.write(f'  ✓ Created {count} payments')
