# University ERP System

A multi-instance, multi-tenant Enterprise Resource Planning platform for higher education institutions with advanced RBAC (Role-Based Access Control).

## 🏗️ Architecture Overview

### Multi-Tenancy Model
- **Tier 1**: University-Level Isolation (separate instances per university)
- **Tier 2**: College-Level Organization (multiple colleges within one university)
- **Tier 3**: Role-Based Access Control (dynamic roles with granular permissions)

### Key Features
✅ **Unified Frontend**: Single React codebase serving all user roles
✅ **Dynamic RBAC**: Superadmin creates custom roles with granular permissions
✅ **Multi-Instance Support**: Each university = independent ERP instance
✅ **College Isolation**: Multiple colleges using `college_id` separation
✅ **BYOD Support**: Bring Your Own Database capability
✅ **Production-Ready Security**: Argon2, JWT (RS256), Redis caching, audit logs

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.0 + Django REST Framework
- **Database**: PostgreSQL 15+
- **Cache/Queue**: Redis + Celery
- **Authentication**: Custom OAuth 2.1 + JWT (RS256)
- **Password Hashing**: Argon2

### Frontend (Planned)
- **Framework**: React 18 + TypeScript
- **State Management**: Redux Toolkit
- **HTTP Client**: Axios
- **Deployment**: Vercel + Cloudflare CDN

### DevOps
- **Containerization**: Docker + Docker Compose
- **Production**: Kubernetes / Docker Swarm
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana + Sentry

## 📦 Project Structure

```
ERP-MAIN-PROJECT/
├── backend/                    # Django backend
│   ├── apps/
│   │   ├── core/              # Abstract models & utilities
│   │   ├── authentication/    # JWT auth & OAuth
│   │   ├── users/             # User model & RBAC
│   │   ├── roles/             # Role & Permission models
│   │   ├── colleges/          # College & Department models
│   │   ├── courses/           # Course management
│   │   ├── attendance/        # Attendance tracking
│   │   ├── finance/           # Fee & payment management
│   │   ├── library/           # Library management
│   │   └── reports/           # Analytics & reporting
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── dev.py
│   │   │   └── prod.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── celery.py
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── dev.txt
│   │   └── prod.txt
│   ├── manage.py
│   └── .env.example
├── frontend/                   # React frontend (to be created)
├── docker/                     # Docker configs
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### 1. Clone & Setup Environment

```bash
cd ERP-MAIN-PROJECT/backend
cp .env.example .env
# Edit .env with your database credentials
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows

# Install requirements
pip install -r requirements/dev.txt
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb erp_university

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Load Initial Data

```bash
# Load default roles and permissions
python manage.py loaddata initial_roles
python manage.py loaddata initial_permissions
```

### 5. Run Development Server

```bash
python manage.py runserver
```

🌐 Access the API at: `http://localhost:8000`
📚 API Documentation: `http://localhost:8000/api/docs/`

## 🐳 Docker Setup

```bash
# Build and start all services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

## 📊 Database Schema

### Core Tables

#### **colleges** - University College/Branch
- `id`, `name`, `code`, `address`, `principal_id`, `is_active`

#### **users** - User accounts with college association
- `id`, `email`, `username`, `first_name`, `last_name`
- `college_id` (FK), `department_id` (FK)
- `is_active`, `is_staff`, `is_superuser`

#### **user_roles** - Dynamic user roles
- `id`, `name`, `description`, `is_default`, `is_system_role`
- `college_id` (optional for college-specific roles)

#### **permissions** - Granular permissions
- `id`, `name`, `codename`, `module`, `description`

#### **role_permissions** - Role-Permission mapping
- `role_id` (FK), `permission_id` (FK), `college_id` (optional)

#### **user_role_assignments** - User-Role assignments
- `user_id` (FK), `role_id` (FK), `college_id` (FK)
- `assigned_by`, `is_active`

#### **students** - Student profiles
- `user_id` (FK), `roll_number`, `enrollment_date`, `current_semester`
- `college_id` (FK), `department_id` (FK)

#### **teachers** - Teacher profiles
- `user_id` (FK), `employee_id`, `hire_date`, `specialization`
- `college_id` (FK), `department_id` (FK)

## 🔐 RBAC System

### Default Roles
1. **Superadmin** - Full ERP control
2. **Admin** - College-level management
3. **Teacher** - Course & attendance management
4. **Student** - Student portal access
5. **Staff** - Support functions

### Custom Roles
Superadmin can create unlimited custom roles (e.g., "Librarian", "HOD", "Accountant") and assign granular permissions.

### Permission System
Permissions follow the pattern: `{action}_{module}`

Examples:
- `view_attendance`, `mark_attendance`
- `create_course`, `edit_course`, `delete_course`
- `manage_users`, `view_reports`

## 🔑 Authentication Flow

1. **Login**: POST `/api/auth/login/` with email & password
2. **Response**: Access token (JWT, 15min) + Refresh token (opaque, 7 days)
3. **Authorization**: Include `Authorization: Bearer <access_token>` in headers
4. **Refresh**: POST `/api/auth/token/refresh/` with refresh token
5. **Logout**: POST `/api/auth/logout/`

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/my-permissions/` - Get current user permissions

### Users
- `GET /api/users/` - List users (with pagination)
- `POST /api/users/` - Create user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Roles
- `GET /api/roles/` - List roles
- `POST /api/roles/` - Create role (Superadmin only)
- `GET /api/roles/{id}/` - Get role details
- `PUT /api/roles/{id}/permissions/` - Assign permissions to role

### Colleges
- `GET /api/colleges/` - List colleges
- `POST /api/colleges/` - Create college
- `GET /api/colleges/{id}/departments/` - List departments

See full API documentation at `/api/docs/`

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users

# With coverage
pytest --cov=apps --cov-report=html
```

## 📝 Development Roadmap

### ✅ Phase 1: Foundation (Current)
- [x] Django project structure
- [x] Core models (User, Role, Permission, College)
- [ ] Authentication system with JWT
- [ ] RBAC middleware & permissions
- [ ] API endpoints for core features

### 🔄 Phase 2: Core Features
- [ ] Superadmin dashboard APIs
- [ ] User management module
- [ ] Role & permission management
- [ ] College & department management
- [ ] Theme & language customization

### 📅 Phase 3: Academic Modules
- [ ] Attendance system
- [ ] Course management
- [ ] Grade management
- [ ] Student/Teacher portals

### 🚀 Phase 4: Advanced Features
- [ ] Finance module
- [ ] Library management
- [ ] Reports & analytics
- [ ] Audit logging
- [ ] Multi-instance deployment automation

### 💻 Phase 5: Frontend
- [ ] React project setup
- [ ] Authentication UI
- [ ] Role-based routing & rendering
- [ ] Dashboard components
- [ ] CRUD interfaces for all modules

## 🔧 Configuration

### Environment Variables

```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_NAME=erp_university
DATABASE_USER=erp_user
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1

# JWT
JWT_ALGORITHM=HS256  # Use RS256 in production
JWT_ACCESS_TOKEN_LIFETIME=900
JWT_REFRESH_TOKEN_LIFETIME=604800

# University Config
UNIVERSITY_NAME=University One
UNIVERSITY_CODE=UNI1
DEPLOYMENT_TYPE=managed
```

## 🛡️ Security Features

- ✅ Argon2 password hashing
- ✅ JWT with RS256 (production) / HS256 (development)
- ✅ Permission caching with Redis
- ✅ CORS protection
- ✅ CSRF protection
- ✅ Rate limiting (planned)
- ✅ Audit logging (planned)
- ✅ Row-level security (planned)

## 📄 License

Proprietary - All rights reserved

## 👥 Contributors

- Development Team

## 📞 Support

For support, email: support@erp-system.com

---

**Note**: This is an active development project. Features are being added incrementally following the roadmap above.
