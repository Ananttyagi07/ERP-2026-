# API Documentation - University ERP System

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All endpoints (except login) require JWT authentication:
```
Authorization: Bearer <access_token>
```

---

## 🔐 Authentication Endpoints

### 1. Login
**POST** `/api/auth/login/`

Authenticate user with email and password.

**Request:**
```json
{
  "email": "admin@university.edu",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "email": "admin@university.edu",
      "username": "admin",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "phone": "+1234567890",
      "avatar_url": "http://localhost:8000/media/avatars/avatar.jpg",
      "college_id": 1,
      "college_name": "Engineering College",
      "college_code": "ENG001",
      "department_id": 1,
      "department_name": "Computer Science",
      "is_superuser": true,
      "is_staff": true,
      "primary_role": {
        "id": 1,
        "name": "Superadmin",
        "description": "Full ERP control"
      },
      "email_verified": true
    },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "dGhpc19pc19yYW5kb21fdG9rZW4="
    },
    "redirect_url": "/superadmin/dashboard"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Invalid credentials",
  "errors": {
    "non_field_errors": ["Invalid credentials"]
  }
}
```

---

### 2. Logout
**POST** `/api/auth/logout/`

Logout user by blacklisting access token and revoking refresh token.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request (Optional):**
```json
{
  "refresh_token": "dGhpc19pc19yYW5kb21fdG9rZW4="
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

### 3. Refresh Token
**POST** `/api/auth/refresh/`

Refresh access token using refresh token (implements token rotation).

**Request:**
```json
{
  "refresh_token": "dGhpc19pc19yYW5kb21fdG9rZW4="
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "bmV3X3JhbmRvbV90b2tlbl9zdHJpbmc="
    }
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "message": "Invalid or revoked refresh token"
}
```

---

### 4. Verify Token
**POST** `/api/auth/verify-token/`

Verify if current access token is valid.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Token is valid",
  "data": {
    "user_id": 1,
    "email": "admin@university.edu",
    "exp": 1699999999,
    "role": "Superadmin",
    "college_id": 1
  }
}
```

---

### 5. My Profile
**GET** `/api/auth/my-profile/`

Get current user's detailed profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "admin@university.edu",
      "username": "admin",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "phone": "+1234567890",
      "avatar_url": "http://localhost:8000/media/avatars/avatar.jpg",
      "college_id": 1,
      "college_name": "Engineering College",
      "college_code": "ENG001",
      "department_id": 1,
      "department_name": "Computer Science",
      "is_superuser": true,
      "is_staff": true,
      "primary_role": {
        "id": 1,
        "name": "Superadmin",
        "description": "Full ERP control"
      },
      "email_verified": true
    }
  }
}
```

---

### 6. My Permissions
**GET** `/api/auth/my-permissions/`

Get current user's permissions (used by frontend to show/hide features).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "admin@university.edu",
      "username": "admin",
      "full_name": "John Doe",
      "role": "Superadmin",
      "role_id": 1,
      "college_id": 1,
      "is_superuser": true
    },
    "permissions": [
      {
        "id": 1,
        "name": "View General Setting",
        "codename": "view_general_setting",
        "module": "setting"
      },
      {
        "id": 2,
        "name": "Add General Setting",
        "codename": "add_general_setting",
        "module": "setting"
      },
      {
        "id": 45,
        "name": "View Student",
        "codename": "view_student",
        "module": "student"
      }
    ]
  }
}
```

---

## 👥 Role Management Endpoints

### 7. List Roles
**GET** `/api/roles/roles/`

Get all roles with counts.

**Query Parameters:**
- `is_default` (boolean): Filter by default roles
- `is_active` (boolean): Filter by active status
- `college_id` (integer): Filter by college

**Example:**
```
GET /api/roles/roles/?is_default=true&is_active=true
```

**Response (200 OK):**
```json
{
  "count": 7,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Superadmin",
      "description": "Full ERP control",
      "is_default": true,
      "is_system_role": true,
      "is_active": true,
      "college_id": null,
      "college_name": null,
      "permissions_count": 150,
      "users_count": 2,
      "created_at": "2025-11-07T10:00:00Z"
    },
    {
      "id": 6,
      "name": "Head Security Guard",
      "description": "Manages security operations",
      "is_default": false,
      "is_system_role": false,
      "is_active": true,
      "college_id": 1,
      "college_name": "Engineering College",
      "permissions_count": 5,
      "users_count": 1,
      "created_at": "2025-11-07T11:00:00Z"
    }
  ]
}
```

---

### 8. Create Role
**POST** `/api/roles/roles/`

Create a new custom role.

**Request:**
```json
{
  "name": "Librarian",
  "description": "Manages library operations",
  "college_id": 1,
  "is_active": true
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Role created successfully",
  "data": {
    "id": 7,
    "name": "Librarian",
    "description": "Manages library operations",
    "college_id": 1,
    "is_active": true
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Invalid data",
  "errors": {
    "name": ["A role with this name already exists"]
  }
}
```

---

### 9. Get Role Details
**GET** `/api/roles/roles/{id}/`

Get detailed information about a specific role including permissions.

**Example:**
```
GET /api/roles/roles/3/
```

**Response (200 OK):**
```json
{
  "id": 3,
  "name": "Teacher",
  "description": "Teaching and course management",
  "is_default": true,
  "is_system_role": true,
  "is_active": true,
  "college_id": null,
  "college_name": null,
  "created_by": null,
  "created_by_name": null,
  "users_count": 45,
  "permissions": [
    {
      "id": 45,
      "name": "View Student",
      "codename": "view_student",
      "description": "View permission for Student",
      "module": "student",
      "created_at": "2025-11-07T10:00:00Z"
    },
    {
      "id": 46,
      "name": "Add Student Attendance",
      "codename": "add_student_attendance",
      "description": "Add permission for Student Attendance",
      "module": "attendance",
      "created_at": "2025-11-07T10:00:00Z"
    }
  ],
  "created_at": "2025-11-07T10:00:00Z",
  "updated_at": "2025-11-07T10:00:00Z"
}
```

---

### 10. Update Role
**PUT** `/api/roles/roles/{id}/`

Update role information (cannot update system roles).

**Request:**
```json
{
  "name": "Senior Librarian",
  "description": "Manages library and archives",
  "college_id": 1,
  "is_active": true
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Role updated successfully",
  "data": {
    "id": 7,
    "name": "Senior Librarian",
    "description": "Manages library and archives",
    "college_id": 1,
    "is_active": true
  }
}
```

**Error Response (403 Forbidden):**
```json
{
  "success": false,
  "message": "System roles cannot be modified"
}
```

---

### 11. Delete Role
**DELETE** `/api/roles/roles/{id}/`

Delete a custom role (cannot delete system roles or roles with active users).

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Role deleted successfully"
}
```

**Error Response (403 Forbidden):**
```json
{
  "success": false,
  "message": "System roles cannot be deleted"
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Cannot delete role. 5 active users are assigned to this role."
}
```

---

## 🔑 Permission Assignment Endpoints

### 12. Get Role Permissions
**GET** `/api/roles/roles/{id}/permissions/`

Get all permissions grouped by module with assignment status for a specific role.

**Example:**
```
GET /api/roles/roles/3/permissions/
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "role": {
      "id": 3,
      "name": "Teacher",
      "description": "Teaching and course management"
    },
    "permissions_by_module": [
      {
        "module": "setting",
        "module_name": "Setting",
        "permissions": [
          {
            "id": 1,
            "name": "View General Setting",
            "codename": "view_general_setting",
            "description": "View permission for General Setting",
            "is_assigned": false
          },
          {
            "id": 2,
            "name": "Add General Setting",
            "codename": "add_general_setting",
            "description": "Add permission for General Setting",
            "is_assigned": false
          }
        ]
      },
      {
        "module": "student",
        "module_name": "Student",
        "permissions": [
          {
            "id": 45,
            "name": "View Student",
            "codename": "view_student",
            "description": "View permission for Student",
            "is_assigned": true
          },
          {
            "id": 46,
            "name": "Add Student",
            "codename": "add_student",
            "description": "Add permission for Student",
            "is_assigned": false
          }
        ]
      }
    ]
  }
}
```

---

### 13. Assign Permissions to Role
**PUT** `/api/roles/roles/{id}/permissions/`

Assign permissions to a role (replaces existing permissions).

**Request:**
```json
{
  "permission_ids": [1, 2, 5, 45, 46, 47, 48, 65, 66, 67, 68]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "11 permissions assigned to role successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Invalid data",
  "errors": {
    "permission_ids": ["Invalid permission IDs: 999, 1000"]
  }
}
```

---

### 14. Bulk Assign Permissions by Module
**POST** `/api/roles/roles/{id}/permissions/bulk/`

Assign permissions in bulk by module.

**Request:**
```json
{
  "permissions": {
    "attendance": [65, 66, 67, 68],
    "student": [45, 46, 47, 48],
    "assignment": [89, 90, 91, 92]
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "12 permissions assigned to role successfully"
}
```

---

## 📋 Permission Endpoints

### 15. List All Permissions
**GET** `/api/roles/permissions/`

Get all permissions with optional filtering.

**Query Parameters:**
- `module` (string): Filter by module name

**Example:**
```
GET /api/roles/permissions/?module=attendance
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "count": 4,
    "permissions": [
      {
        "id": 65,
        "name": "View Student Attendance",
        "codename": "view_student_attendance",
        "description": "View permission for Student Attendance",
        "module": "attendance",
        "created_at": "2025-11-07T10:00:00Z"
      },
      {
        "id": 66,
        "name": "Add Student Attendance",
        "codename": "add_student_attendance",
        "description": "Add permission for Student Attendance",
        "module": "attendance",
        "created_at": "2025-11-07T10:00:00Z"
      }
    ]
  }
}
```

---

### 16. Get Permission Modules
**GET** `/api/roles/permissions/modules/`

Get list of all modules with permission counts.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "count": 37,
    "modules": [
      {
        "module": "setting",
        "module_name": "Setting",
        "permission_count": 28
      },
      {
        "module": "student",
        "module_name": "Student",
        "permission_count": 4
      },
      {
        "module": "attendance",
        "module_name": "Attendance",
        "permission_count": 8
      }
    ]
  }
}
```

---

### 17. Get Grouped Permissions
**GET** `/api/roles/permissions/grouped/`

Get all permissions grouped by module (useful for frontend checkboxes).

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "permissions_by_module": [
      {
        "module": "setting",
        "module_name": "Setting",
        "permissions": [
          {
            "id": 1,
            "name": "View General Setting",
            "codename": "view_general_setting",
            "description": "View permission for General Setting"
          }
        ]
      }
    ]
  }
}
```

---

## 🔍 Common Response Codes

| Status Code | Description |
|-------------|-------------|
| 200 OK | Request succeeded |
| 201 Created | Resource created successfully |
| 400 Bad Request | Invalid request data |
| 401 Unauthorized | Authentication failed or token expired |
| 403 Forbidden | User doesn't have permission |
| 404 Not Found | Resource not found |
| 500 Internal Server Error | Server error |

---

## 📝 Notes

### Token Expiry
- **Access Token**: 15 minutes (900 seconds)
- **Refresh Token**: 7 days (604800 seconds)

### Token Rotation
When refreshing a token, the old refresh token is automatically revoked and replaced with a new one for security.

### Permission Caching
User permissions are cached in Redis for 5 minutes. Cache is automatically invalidated when:
- User roles are changed
- Role permissions are modified
- User logs out

### College Isolation
Non-superuser users can only see and manage:
- System roles (college_id = null)
- Roles belonging to their college

---

## 🚀 Usage Examples

### Example 1: Login Flow
```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@university.edu",
    "password": "password123"
  }'

# Save the access_token and refresh_token from response

# 2. Use access token for API calls
curl -X GET http://localhost:8000/api/auth/my-permissions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 3. When access token expires, refresh it
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

### Example 2: Create Custom Role and Assign Permissions
```bash
# 1. Create custom role
curl -X POST http://localhost:8000/api/roles/roles/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Librarian",
    "description": "Manages library operations",
    "college_id": 1
  }'

# Response will include role_id (e.g., 7)

# 2. Get all available permissions
curl -X GET http://localhost:8000/api/roles/permissions/grouped/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 3. Assign specific permissions to the role
curl -X PUT http://localhost:8000/api/roles/roles/7/permissions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "permission_ids": [53, 54, 55, 56, 57, 58, 59, 60]
  }'
```

### Example 3: Check User Permissions
```bash
# Get current user's permissions
curl -X GET http://localhost:8000/api/auth/my-permissions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Frontend can use this response to:
# - Show/hide menu items
# - Enable/disable buttons
# - Control access to features
```

---

## 📊 Database Seeding

Before using the API, seed the database with permissions:

```bash
cd backend
source venv/bin/activate
python manage.py seed_permissions
```

This creates:
- ✅ All 37 modules
- ✅ 600+ permissions (4 per feature: view, add, edit, delete)
- ✅ 5 default roles (Superadmin, Admin, Teacher, Student, Staff)

---

## 🎯 Next API Endpoints (Coming Soon)

1. **Superadmin Management**
   - POST /api/superadmin/
   - PUT /api/superadmin/{id}/
   - GET /api/superadmin/

2. **User Management**
   - POST /api/users/reset-password/
   - POST /api/users/reset-username/
   - GET /api/users/credentials/

3. **Template Management**
   - CRUD for SMS templates
   - CRUD for Email templates

4. **Front Office Module**
   - Visitor management
   - Call logs
   - Postal dispatch/receive

5. **HR Module**
   - Designation management
   - Employee management

---

**Last Updated**: 2025-11-07
**API Version**: v1.0
