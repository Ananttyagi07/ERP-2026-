# ERP System Setup Instructions

## 🚀 Quick Setup Guide

### Step 1: Restore Your PostgreSQL Databases

You have two database files from your friend. Let's restore them:

```bash
# Create directory for database dumps
mkdir -p database_dumps
cp ~/Downloads/Erp_Database database_dumps/
cp ~/Downloads/Erp_Databaseplain database_dumps/

# Start Docker containers
docker-compose up -d postgres redis

# Wait for PostgreSQL to be ready
sleep 10

# Restore the database
docker-compose exec postgres pg_restore -U erp_user -d erp_university /database_dumps/Erp_Database

# OR if using plain text dump:
docker-compose exec postgres psql -U erp_user -d erp_university < database_dumps/Erp_Databaseplain
```

### Step 2: Set Up Python Environment (Local Development)

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements/dev.txt

# Copy environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

### Step 3: Database Migrations

Since you already have a database from your friend, you have two options:

**Option A: Use Existing Database** (Recommended for testing)
```bash
# Just connect to the restored database
python manage.py inspectdb > apps/temp_models.py
# This will generate models from your existing database
```

**Option B: Fresh Start with Our Models**
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create initial data
python manage.py create_default_roles
python manage.py create_superuser
```

### Step 4: Start Development Server

```bash
# Start backend
python manage.py runserver

# In another terminal, start Celery (optional)
celery -A config worker -l info
```

## 📊 Database Connection

Your `.env` file should have:

```env
DATABASE_NAME=erp_university
DATABASE_USER=erp_user
DATABASE_PASSWORD=erp_password
DATABASE_HOST=localhost  # or 'postgres' if using Docker
DATABASE_PORT=5432
```

## 🔐 Authentication Flow (As You Requested)

### 1. **Login Request**

**Endpoint**: `POST /api/auth/login/`

**Request Body**:
```json
{
  "email": "superadmin@university.edu",
  "password": "your_password"
}
```

**Backend Process**:
1. ✅ Check if email exists in database
2. ✅ Verify password hash (Argon2)
3. ✅ Check if user is_active = True
4. ✅ Get user's role from `user_role_assignments` table
5. ✅ Get user's permissions from role
6. ✅ Generate JWT access token (15 min)
7. ✅ Generate opaque refresh token (7 days)
8. ✅ Return user info + tokens

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "email": "superadmin@university.edu",
      "username": "superadmin",
      "full_name": "John Doe",
      "college_id": 1,
      "college_name": "Main Campus",
      "college_code": "MAIN",
      "is_superuser": true,
      "primary_role": {
        "id": 1,
        "name": "Superadmin",
        "description": "Full system control"
      }
    },
    "tokens": {
      "access": "eyJhbGciOiJIUzI1NiIs...",
      "refresh": "c3VwZXJzZWNyZXRyZWZy..."
    }
  }
}
```

**Response** (400 Bad Request - Invalid Credentials):
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

### 2. **Get User Permissions**

**Endpoint**: `GET /api/auth/my-permissions/`

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response**:
```json
{
  "user": {
    "id": 1,
    "email": "superadmin@university.edu",
    "role": "Superadmin",
    "college_id": 1
  },
  "permissions": [
    {"id": 1, "name": "View Dashboard", "codename": "view_dashboard", "module": "dashboard"},
    {"id": 2, "name": "Manage Users", "codename": "manage_users", "module": "users"},
    {"id": 3, "name": "Manage Roles", "codename": "manage_roles", "module": "roles"},
    {"id": 4, "name": "Manage Colleges", "codename": "manage_colleges", "module": "colleges"},
    {"id": 5, "name": "View Theme Settings", "codename": "view_theme", "module": "theme"},
    {"id": 6, "name": "Manage Theme", "codename": "manage_theme", "module": "theme"},
    {"id": 7, "name": "Manage Languages", "codename": "manage_languages", "module": "language"}
    // ... all other permissions
  ]
}
```

### 3. **Frontend Portal Routing Based on Role**

After login, frontend checks `user.primary_role.name`:

```javascript
// Frontend logic (pseudo-code)
if (user.primary_role.name === 'Superadmin') {
  redirect('/superadmin/dashboard')
  // Show: Dashboard, Theme, Language, Administrator menu
}
else if (user.primary_role.name === 'Admin') {
  redirect('/admin/dashboard')
  // Show: College-specific features
}
else if (user.primary_role.name === 'Teacher') {
  redirect('/teacher/dashboard')
  // Show: Courses, Attendance, Grades
}
else if (user.primary_role.name === 'Student') {
  redirect('/student/dashboard')
  // Show: My Courses, My Attendance, Results
}
```

## 🎨 Superadmin Features Implementation Status

### ✅ Completed (Backend Core)
- [x] User authentication with JWT
- [x] Role-based access control (RBAC)
- [x] Permission system
- [x] College/School multi-tenancy
- [x] User management models

### 🔄 In Progress (APIs to build)
- [ ] Dashboard API (user stats, graphs, calendar)
- [ ] Theme management API
- [ ] Language management API
- [ ] General Settings API
- [ ] School/College management API
- [ ] Payment settings API
- [ ] SMS/Email settings API
- [ ] Academic year API
- [ ] Role & Permission management API

## 📁 Project Structure Created

```
backend/
├── apps/
│   ├── core/           ✅ Base models (TimeStamped, SoftDelete)
│   ├── authentication/ ✅ JWT, Login, Tokens
│   ├── users/          ✅ User, Student, Teacher models
│   ├── roles/          ✅ Role, Permission, RolePermission
│   ├── colleges/       ✅ College, Department models
│   ├── courses/        ⏳ To be built
│   ├── attendance/     ⏳ To be built
│   ├── finance/        ⏳ To be built
│   ├── library/        ⏳ To be built
│   └── reports/        ⏳ To be built
├── config/
│   ├── settings/       ✅ Base, Dev, Prod settings
│   ├── urls.py         ✅ URL routing
│   ├── wsgi.py         ✅ Production server
│   └── celery.py       ✅ Background tasks
├── requirements/       ✅ Dependencies
├── manage.py           ✅ Django CLI
└── .env.example        ✅ Environment template
```

## 🗄️ Database Tables Created

✅ Core Tables:
- `colleges` - College/School information
- `departments` - Academic departments
- `users` - User accounts with college association
- `user_roles` - Dynamic user roles (Superadmin, Admin, Teacher, Student, etc.)
- `permissions` - Granular permissions (view_*, create_*, edit_*, delete_*)
- `role_permissions` - Role-Permission mapping
- `user_role_assignments` - User-Role assignments
- `students` - Student profiles
- `teachers` - Teacher profiles
- `refresh_tokens` - Opaque refresh tokens
- `blacklisted_tokens` - Revoked JWT tokens

## 🔑 Default Roles to Create

Run this command to create default roles:

```bash
python manage.py shell
```

```python
from apps.roles.models import Role, Permission
from apps.colleges.models import College

# Create default roles
roles = [
    {'name': 'Superadmin', 'description': 'Full ERP control', 'is_system_role': True, 'is_default': True},
    {'name': 'Admin', 'description': 'College-level management', 'is_system_role': True, 'is_default': True},
    {'name': 'Teacher', 'description': 'Teaching and course management', 'is_system_role': True, 'is_default': True},
    {'name': 'Student', 'description': 'Student portal access', 'is_system_role': True, 'is_default': True},
    {'name': 'Staff', 'description': 'Support staff', 'is_system_role': True, 'is_default': True},
]

for role_data in roles:
    Role.objects.get_or_create(**role_data)
```

## 📝 Next Steps

1. **Test Database Connection**:
   - Restore your friend's database
   - Check if data loads correctly
   - Map existing schema to our models

2. **Build Authentication Views**:
   - Complete login/logout endpoints
   - Test JWT token generation
   - Verify permission loading

3. **Create Superadmin APIs**:
   - Dashboard statistics
   - Theme management
   - Language management
   - School management

4. **Testing**:
   - Test login with existing users
   - Verify role-based access
   - Check permission enforcement

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres

# Connect to database manually
docker-compose exec postgres psql -U erp_user -d erp_university
```

### Migration Issues
```bash
# Reset migrations (careful!)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

## 📞 Need Help?

If you encounter any issues:
1. Check logs in `backend/logs/django.log`
2. Verify database connectivity
3. Ensure all environment variables are set
4. Check if Redis is running (for caching)

---

**Status**: Backend foundation complete ✅
**Next Phase**: API endpoints for Superadmin features 🚧
