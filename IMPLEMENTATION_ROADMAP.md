# University ERP System - Complete Implementation Roadmap

## 📚 Documentation Overview

This document tracks **every step** of the implementation process, what's been built, and what comes next.

---

## 🎯 Project Vision

A **multi-instance, multi-tenant** University ERP system where:
- Each university = independent instance
- Multiple colleges within one university
- Dynamic role-based access control (RBAC)
- Unified frontend for all user types
- Permission-based feature visibility

---

## ✅ Phase 1: Foundation (COMPLETED)

### Step 1.1: Project Structure Setup ✅
**Date**: Nov 7, 2025
**Files Created**:
- `README.md` - Project overview
- `QUICKSTART.md` - Quick start guide
- `SETUP_INSTRUCTIONS.md` - Detailed setup
- `PROJECT_STATUS.md` - Current status
- `docker-compose.yml` - Docker orchestration
- `setup.sh` - Automated setup script

**What It Does**:
- Provides complete project documentation
- Sets up development environment
- Explains architecture and features

**How to Use**:
```bash
# Read the documentation
cat README.md
cat QUICKSTART.md

# Run automated setup
./setup.sh
```

---

### Step 1.2: Django Backend Structure ✅
**Files Created**:
```
backend/
├── config/
│   ├── settings/
│   │   ├── base.py      ✅ Base Django settings
│   │   ├── dev.py       ✅ Development settings
│   │   └── prod.py      ✅ Production settings
│   ├── urls.py          ✅ URL routing
│   ├── wsgi.py          ✅ Production server
│   ├── asgi.py          ✅ ASGI server
│   └── celery.py        ✅ Background tasks
├── requirements/
│   ├── base.txt         ✅ Core dependencies
│   ├── dev.txt          ✅ Dev dependencies
│   └── prod.txt         ✅ Prod dependencies
├── manage.py            ✅ Django CLI
├── .env.example         ✅ Environment template
└── Dockerfile           ✅ Container definition
```

**What It Does**:
- Multi-environment configuration (dev/prod)
- Django REST Framework setup
- PostgreSQL + Redis + Celery configured
- Security settings (CORS, CSRF, Argon2)

**How to Use**:
```bash
cd backend
cp .env.example .env
# Edit .env with your database credentials
source venv/bin/activate
pip install -r requirements/dev.txt
```

---

### Step 1.3: Core Database Models ✅
**Files Created**:
- `apps/core/models.py` - Base abstract models
- `apps/colleges/models.py` - College & Department
- `apps/users/models.py` - User, Student, Teacher
- `apps/roles/models.py` - Role, Permission, RolePermission

**Models Created**:

#### 1. Core Abstract Models
```python
# TimeStampedModel - Adds created_at, updated_at
# SoftDeleteModel - Adds is_deleted, deleted_at
# CollegeIsolatedModel - Adds college_id foreign key
```

#### 2. College Models
```python
# College - University college/branch
#   - name, code, address, principal, is_active
# Department - Academic department
#   - college_id, name, code, head, is_active
```

#### 3. User Models
```python
# User - Custom user with college association
#   - email, username, password (Argon2)
#   - college_id, department_id
#   - is_active, is_staff, is_superuser
#   - Methods: get_permissions(), has_permission()
#
# UserRoleAssignment - User ↔ Role junction
#   - user_id, role_id, college_id, is_active
#
# Student - Extended student profile
#   - user_id, roll_number, enrollment_date
#
# Teacher - Extended teacher profile
#   - user_id, employee_id, hire_date
```

#### 4. Role & Permission Models
```python
# Permission - Granular permissions
#   - name, codename, module, description
#
# Role - Dynamic user roles
#   - name, description, is_default, is_system_role
#   - college_id (optional), created_by
#
# RolePermission - Role ↔ Permission junction
#   - role_id, permission_id, assigned_by
```

**Database Tables**:
- ✅ `colleges` - College information
- ✅ `departments` - Academic departments
- ✅ `users` - User accounts
- ✅ `user_roles` - Role definitions
- ✅ `permissions` - Permission definitions
- ✅ `role_permissions` - Role-permission mappings
- ✅ `user_role_assignments` - User-role assignments
- ✅ `students` - Student profiles
- ✅ `teachers` - Teacher profiles
- ✅ `refresh_tokens` - Refresh tokens
- ✅ `blacklisted_tokens` - Revoked tokens

**How to Use**:
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check tables
python manage.py dbshell
\dt
```

---

### Step 1.4: Authentication System ✅
**Files Created**:
- `apps/authentication/models.py` - RefreshToken, BlacklistedToken
- `apps/authentication/jwt_utils.py` - JWT generation/validation
- `apps/authentication/backends.py` - Custom JWT authentication
- `apps/authentication/middleware.py` - Permission middleware
- `apps/authentication/serializers.py` - Login, User, Permission serializers

**Features Implemented**:
1. **JWT Token Generation**
   - Algorithm: HS256 (configurable to RS256)
   - Access Token: 15 minutes expiry
   - Includes: user_id, email, role, college_id

2. **Refresh Token System**
   - Opaque tokens stored in database
   - 7 days expiry
   - Token rotation support
   - Revocation support

3. **Token Blacklisting**
   - Immediate token revocation
   - Cached in Redis for performance

4. **Custom Authentication Backend**
   - Extracts JWT from Authorization header
   - Validates token signature and expiry
   - Checks blacklist
   - Loads user from database

5. **Permission Middleware**
   - Loads user permissions on request
   - Caches permissions in Redis (5 min)
   - Adds `request.has_permission()` helper

**Authentication Flow**:
```
1. User sends email + password to /api/auth/login/
2. Backend validates credentials
3. Checks is_active flag
4. Loads user's role and permissions
5. Generates JWT access token (15 min)
6. Generates opaque refresh token (7 days)
7. Returns user info + tokens
8. Frontend stores tokens
9. Frontend includes "Authorization: Bearer <token>" in requests
10. Backend validates token on each request
11. Backend loads permissions and enforces access control
```

**How to Use**:
```python
# In views
from apps.authentication.jwt_utils import JWTHandler

# Generate token
token = JWTHandler.generate_access_token(user)

# Validate token
payload = JWTHandler.decode_access_token(token)

# Blacklist token
JWTHandler.blacklist_token(token, user, reason="User logged out")
```

---

### Step 1.5: ACL (Access Control List) System ✅
**Files Created**:
- `apps/roles/serializers.py` - Role & Permission serializers
- `apps/roles/management/commands/seed_permissions.py` - Database seeder
- `ACL_SYSTEM_GUIDE.md` - Complete ACL documentation

**What It Does**:
Creates a complete permission system with **37 modules** and **600+ permissions**.

#### All 37 Modules Implemented:
1. **Setting** (7 features)
   - General Setting, Payment Setting, SMS Setting, Email Setting
   - Global Search, Global Session Change, Opening Hour

2. **Theme** (1 feature)
   - Theme management

3. **Language** (1 feature)
   - Multi-language support

4. **Administrator** (16 features)
   - Academic Year, User Role, Role Permission, Manage User
   - Reset User Password, Backup Database, School Management
   - Payment Gateway, SMS Gateway, SMS/Email Templates
   - Activity Log, Super Admin, Guardian Feedback, User Credential

5. **Human Resource** (2 features)
   - Designation, Employee

6. **Teacher** (4 features)
   - Teacher, Teacher Lecture, Department, Rating

7. **Academic Activity** (10 features)
   - Classes, Section, Subject, Syllabus, Class Routine
   - Promotion, Material, Live Class, Assignment, Submission

8. **Guardian** (2 features)
   - Guardian, Feedback

9. **Student** (5 features)
   - Student, Bulk Import, Student Activity, Online Admission, Student Type

10. **Attendance** (5 features)
    - Employee/Teacher/Student Attendance, Absent Email/SMS

11. **Exam** (5 features)
    - Exam Term, Grade, Schedule, Suggestion, Exam Attendance

12. **Exam Mark** (11 features)
    - Exam Mark, Mark Sheet, Result, Mark SMS/Email
    - Exam Result, Final Result, Merit List, Result Email/SMS/Card

13. **Library** (4 features)
    - Library Book, Library Member, Issue & Return, e-book

14. **Transport** (3 features)
    - Vehicle, Transport Route, Transport Member

15. **Hostel** (3 features)
    - Hostel, Hostel Room, Hostel Member

16. **Message, Email & SMS** (3 features)
    - Email, Text SMS, Message

17. **Announcement** (3 features)
    - Notice, News, Holiday

18. **Event** (1 feature)
    - Event management

19. **Front Office** (6 features)
    - Visitor, Visitor Purpose, Call Logs
    - Postal Dispatch, Postal Receive, Front Office

20. **Accounting** (11 features)
    - Expenditure Head/Expenditure, Income Head/Income
    - Invoice, Payment, Discount, Fee Type
    - Due Fee Email/SMS, Invoice Receipt

21. **Report** (1 feature)
    - Report generation

22. **Certificate** (2 features)
    - Certificate Type, Certificate

23. **Media Gallery** (2 features)
    - Gallery, Image

24. **Frontend** (3 features)
    - Frontend CMS, Home Slider, About

25. **Payroll** (3 features)
    - Salary Grade, Payment, History

26. **Complain** (2 features)
    - Complain, Complain Type

27. **User Complain** (1 feature)
    - User Complain (Except Super Admin)

28. **User Leave** (1 feature)
    - User Leave (Except Super Admin)

29. **Leave Management** (6 features)
    - Leave Management, Leave Type, Leave Application
    - Waiting/Approve/Decline Leave

30. **ID Card & Admit Card** (9 features)
    - ID/Admit card, Teacher/Employee/Student ID card
    - ID Card/Admit Card Settings (Superadmin/Admin)

31. **Miscellaneous** (3 features)
    - Award, FAQ, Todo

32. **Scholarship** (3 features)
    - Candidate, Donar, Scholarship

33. **Asset Management** (6 features)
    - Category, Issue, Item Category, Purchase, Store, Vendor

34. **Inventory** (7 features)
    - Item Category, Supplier, Warehouse, Product
    - Item Purchase, Sale, Issue

35. **Lessonplan** (5 features)
    - Lessonplan, Lesson, Topic, Status, Timeline

36. **Online Exam** (4 features)
    - Take Exam, Online Exam, Question Bank, Exam Instructions

37. **Subscription** (5 features)
    - FAQs, Slider, Subscription, Setting, Plan (Only Superadmin)

**Permission Structure**:
Each feature has 4 permissions:
- `view_{feature}` - Can view the feature
- `add_{feature}` - Can create new records
- `edit_{feature}` - Can modify existing records
- `delete_{feature}` - Can delete records

**Example**:
```python
# Library module permissions:
view_library_book
add_library_book
edit_library_book
delete_library_book
view_library_member
add_library_member
edit_library_member
delete_library_member
view_issue_return
add_issue_return
edit_issue_return
delete_issue_return
view_ebook
add_ebook
edit_ebook
delete_ebook
```

**How to Use**:
```bash
# Seed all permissions
python manage.py seed_permissions

# Output:
# ✓ Created: view_general_setting
# ✓ Created: add_general_setting
# ... (600+ permissions)
# ✓ Created role: Superadmin
# ✓ Created role: Admin
# ✓ Created role: Teacher
# ✓ Created role: Student
# ✓ Created role: Staff
```

**Check the Data**:
```bash
python manage.py shell
```

```python
from apps.roles.models import Permission, Role
from django.db.models import Count

# Total permissions
print(f"Total: {Permission.objects.count()}")

# Permissions by module
modules = Permission.objects.values('module').annotate(count=Count('id'))
for m in modules:
    print(f"{m['module']}: {m['count']} permissions")

# Roles
for role in Role.objects.all():
    print(f"{role.name} - {role.description}")
```

---

## 🔄 Phase 2: API Development (CURRENT)

### Step 2.1: Role Management Serializers ✅
**File**: `apps/roles/serializers.py`

**Serializers Created**:
1. `RoleListSerializer` - List view with counts
2. `RoleCreateSerializer` - Create/edit roles
3. `RoleDetailSerializer` - Detailed view with permissions
4. `RolePermissionAssignSerializer` - Assign permissions
5. `PermissionSerializer` - Permission details
6. `PermissionGroupedSerializer` - Permissions grouped by module

**What They Do**:
- List all roles (default + custom)
- Create custom roles (e.g., "Librarian", "Security Guard")
- View role details with permission count
- Assign/remove permissions from roles
- Group permissions by module for UI

---

### Step 2.2: API Views (PENDING) 🔄

**Next Task**: Build the actual API views for role management

**Files to Create**:
- `apps/roles/views.py` - ViewSets for CRUD operations
- `apps/roles/urls.py` - URL routing
- `apps/authentication/views.py` - Login/logout views
- `apps/authentication/urls.py` - Auth URL routing

**Endpoints Needed**:

#### Role Management
```
GET    /api/roles/                    # List all roles
POST   /api/roles/                    # Create new role
GET    /api/roles/{id}/               # Get role details
PUT    /api/roles/{id}/               # Update role
DELETE /api/roles/{id}/               # Delete role (if not system)
```

#### Permission Management
```
GET    /api/permissions/              # List all permissions (grouped by module)
GET    /api/permissions/modules/      # Get all modules
```

#### Role-Permission Assignment
```
GET    /api/roles/{id}/permissions/   # Get permissions for role (with status)
PUT    /api/roles/{id}/permissions/   # Assign permissions to role
```

#### Authentication
```
POST   /api/auth/login/               # User login
POST   /api/auth/logout/              # User logout
POST   /api/auth/refresh/             # Refresh access token
GET    /api/auth/my-permissions/      # Get current user permissions
```

---

## 📊 Current Status Summary

### ✅ Completed (100%)
- [x] Project documentation
- [x] Django project structure
- [x] Docker containerization
- [x] Database models (all core tables)
- [x] Authentication system (JWT + refresh tokens)
- [x] Permission middleware
- [x] ACL system with 37 modules
- [x] Database seeder (600+ permissions)
- [x] Serializers for roles and permissions

### 🔄 In Progress (0%)
- [ ] API views for role management
- [ ] API views for permission assignment
- [ ] API views for authentication (login/logout)

### 📅 Pending
- [ ] Superadmin dashboard API
- [ ] Theme management API
- [ ] Language management API
- [ ] School/College management API
- [ ] User management API
- [ ] All 37 module APIs
- [ ] Frontend (React) development

---

## 🚀 Quick Start - What You Can Do Now

### 1. Restore Your Database
```bash
cd /home/anant/ERP-MAIN-PROJECT

# Start Docker
docker-compose up -d postgres redis

# Restore database
docker-compose exec -T postgres psql -U erp_user -d erp_university < ~/Downloads/Erp_Databaseplain
```

### 2. Setup Backend
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt
```

### 3. Seed Permissions
```bash
# This creates all 37 modules + 600+ permissions + 5 default roles
python manage.py seed_permissions
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
# Email: admin@test.com
# Password: admin123
```

### 5. Run Server
```bash
python manage.py runserver
# Access: http://localhost:8000
```

---

## 📚 Documentation Files Reference

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | Project overview | ✅ Complete |
| `QUICKSTART.md` | 5-minute setup guide | ✅ Complete |
| `SETUP_INSTRUCTIONS.md` | Detailed setup instructions | ✅ Complete |
| `PROJECT_STATUS.md` | What's built, what's next | ✅ Complete |
| `ACL_SYSTEM_GUIDE.md` | ACL implementation guide | ✅ Complete |
| `IMPLEMENTATION_ROADMAP.md` | This file | ✅ Complete |
| `docker-compose.yml` | Docker orchestration | ✅ Complete |
| `setup.sh` | Automated setup script | ✅ Complete |

---

## 🎯 What to Follow Next

### Step 1: Read the Documentation
```bash
# Start here
cat QUICKSTART.md

# Then read detailed setup
cat SETUP_INSTRUCTIONS.md

# Understand the ACL system
cat ACL_SYSTEM_GUIDE.md

# Check current status
cat PROJECT_STATUS.md
```

### Step 2: Run the Setup Script
```bash
./setup.sh
# This automates the entire setup process
```

### Step 3: Seed the Database
```bash
cd backend
source venv/bin/activate
python manage.py seed_permissions
```

### Step 4: Test Authentication Flow
```bash
# Start server
python manage.py runserver

# In another terminal, test login (once API views are built)
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "password": "admin123"}'
```

---

## 🛠️ Technical Stack

| Component | Technology | Status |
|-----------|-----------|--------|
| **Backend** | Django 5.0 + DRF | ✅ Setup |
| **Database** | PostgreSQL 15 | ✅ Setup |
| **Cache** | Redis 7 | ✅ Setup |
| **Queue** | Celery | ✅ Setup |
| **Auth** | Custom JWT (HS256/RS256) | ✅ Built |
| **Password** | Argon2 | ✅ Configured |
| **API Docs** | DRF Spectacular | ✅ Configured |
| **Container** | Docker + Docker Compose | ✅ Setup |
| **Frontend** | React 18 (Planned) | ⏳ Pending |

---

## 💡 Key Concepts

### Multi-Tenancy Model
```
University (Instance Level)
├── College 1 (college_id: 1)
│   ├── Department A
│   ├── Department B
│   └── Users (filtered by college_id)
├── College 2 (college_id: 2)
│   ├── Department C
│   └── Users (filtered by college_id)
└── College N
```

### Permission Flow
```
1. Superadmin creates role "Librarian"
2. Superadmin assigns permissions:
   - view_library_book
   - add_library_book
   - view_issue_return
   - add_issue_return
3. Admin assigns "Librarian" role to user@university.edu
4. User logs in
5. Backend returns permissions
6. Frontend shows ONLY Library menu
7. Backend enforces permissions on API calls
```

### Database Isolation
```sql
-- All data queries automatically filtered by college_id
SELECT * FROM students WHERE college_id = 1;
SELECT * FROM teachers WHERE college_id = 1;
SELECT * FROM courses WHERE college_id = 1;

-- Row-Level Security (optional enhancement)
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
CREATE POLICY college_isolation ON students
  USING (college_id IN (
    SELECT college_id FROM user_role_assignments
    WHERE user_id = current_user_id
  ));
```

---

## ✅ Checklist for Next Session

- [ ] Build Role Management API views
- [ ] Build Permission Assignment API
- [ ] Build Authentication API views (login/logout)
- [ ] Test with Postman/curl
- [ ] Connect to your restored database
- [ ] Test role creation and permission assignment
- [ ] Test user login with different roles
- [ ] Verify permission enforcement

---

**Last Updated**: Nov 7, 2025
**Current Phase**: API Development
**Next Task**: Build API views for role management
**Completion**: ~40% of backend foundation complete
