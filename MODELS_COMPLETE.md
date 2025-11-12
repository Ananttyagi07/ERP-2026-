# Complete Database Models for University ERP

This document contains all database models for the superadmin features up to Guardian management.

## Implementation Strategy

I'm creating all models in their respective Django apps:
1. `apps/superadmin` - SuperAdminProfile
2. `apps/templates` - SMSTemplate, EmailTemplate
3. `apps/front_office` - VisitorPurpose, VisitorInfo, CallLog, PostalDispatch, PostalReceive
4. `apps/hr` - Designation, Employee
5. `apps/teachers` - Department, Teacher, TeacherLecture, Rating
6. `apps/leave_management` - LeaveType, LeaveApplication
7. `apps/academic` - SchoolClass, ClassSection, Subject, Syllabus, StudyMaterial
8. `apps/live_classes` - LiveClass, LiveClassType, Assignment
9. `apps/students` - Student, StudentParent (relationship)
10. `apps/guardians` - Guardian

## Note on User vs Profile Models

Following Django best practices:
- **User** model (`apps/users/models.py`) - Already exists for authentication
- **Profile** models (in each app) - Extended information specific to each user type

For example:
- Superadmin = User (base) + SuperAdminProfile (extended info)
- Teacher = User (base) + Teacher (extended info)
- Student = User (base) + Student (extended info)
- Guardian = User (base) + Guardian (extended info)

This allows:
- Single authentication table
- Polymorphic user types
- Clean separation of concerns
