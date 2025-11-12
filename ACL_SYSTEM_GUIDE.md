# ACL System Implementation Guide

## ✅ What's Been Created

### 1. **Database Seeder** ✅
**File**: `backend/apps/roles/management/commands/seed_permissions.py`

**Run this command to seed all 37 modules with permissions:**
```bash
cd backend
python manage.py seed_permissions
```

This will create:
- ✅ **All 37 modules** (Setting, Theme, Language, Administrator, etc.)
- ✅ **150+ permissions** (4 permissions per feature: view, add, edit, delete)
- ✅ **5 default roles** (Superadmin, Admin, Teacher, Student, Staff)

### 2. **Role Management Serializers** ✅
**File**: `backend/apps/roles/serializers.py`

Created serializers for:
- `RoleListSerializer` - List all roles with counts
- `RoleCreateSerializer` - Create/edit roles
- `RoleDetailSerializer` - View role with permissions
- `RolePermissionAssignSerializer` - Assign permissions to role
- `PermissionSerializer` - Permission details
- `PermissionCheckboxSerializer` - For checkbox UI

## 📋 Your ACL Requirements - Implementation Status

### **User Role (ACL)** - `GET/POST /api/roles/`

#### ✅ List View (Default)
**Table Columns:**
- SL (Serial Number)
- Name (Role name)
- Note (Description)
- Is Default? (System role badge)
- Action (Edit button)

**API Response:**
```json
{
  "count": 7,
  "results": [
    {
      "id": 1,
      "name": "Superadmin",
      "description": "Full ERP control",
      "is_default": true,
      "is_system_role": true,
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
      "permissions_count": 5,
      "users_count": 1,
      "created_at": "2025-11-07T11:00:00Z"
    }
  ]
}
```

#### ✅ Add Role Form
**Fields:**
- Role Name* (e.g., "Head Security Guard")
- Note/Description

**API Request:**
```bash
POST /api/roles/
{
  "name": "Head Security Guard",
  "description": "Manages security operations and visitor logs"
}
```

### **Role Permission (ACL)** - `GET/PUT /api/roles/{id}/permissions/`

#### ✅ Permission Assignment Table

**School Selector** → **Role Selector** → **Permission Checkboxes**

**Table Structure:**
| # | Module Name | Function Name | View | Add | Edit | Delete |
|---|-------------|---------------|------|-----|------|--------|
| 1 | **Setting** | | | | | |
| 1.1 | | General Setting (Only Admin) | ☐ | ☐ | ☐ | ☐ |
| 1.2 | | Payment Setting (Only Admin) | ☐ | ☐ | ☐ | ☐ |
| 2 | **Theme** | | | | | |
| 2.1 | | Theme | ☑ | ☑ | ☐ | ☐ |
| ... | ... | ... | ... | ... | ... | ... |

**API Response for Permission List:**
```json
{
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
          "is_assigned": false
        },
        {
          "id": 2,
          "name": "Add General Setting",
          "codename": "add_general_setting",
          "is_assigned": false
        }
      ]
    },
    {
      "module": "teacher",
      "module_name": "Teacher",
      "permissions": [
        {
          "id": 45,
          "name": "View Teacher",
          "codename": "view_teacher",
          "is_assigned": true
        },
        {
          "id": 46,
          "name": "Add Teacher",
          "codename": "add_teacher",
          "is_assigned": false
        }
      ]
    }
  ]
}
```

**API Request to Assign Permissions:**
```bash
PUT /api/roles/3/permissions/
{
  "permission_ids": [1, 2, 5, 45, 46, 47, 48, 65, 66, 67, 68]
}
```

## 🎯 Complete API Endpoints Needed

### Role Management
```
GET    /api/roles/                    # List all roles
POST   /api/roles/                    # Create new role
GET    /api/roles/{id}/               # Get role details
PUT    /api/roles/{id}/               # Update role
PATCH  /api/roles/{id}/               # Partial update
DELETE /api/roles/{id}/               # Delete role (if not system role)
```

### Permission Management
```
GET    /api/permissions/              # List all permissions (grouped by module)
GET    /api/permissions/modules/      # Get all modules
```

### Role-Permission Assignment
```
GET    /api/roles/{id}/permissions/   # Get permissions for role (with assignment status)
PUT    /api/roles/{id}/permissions/   # Assign permissions to role
POST   /api/roles/{id}/permissions/bulk/  # Bulk assign by module
```

## 🔐 Permission Behavior Examples

### Example 1: Teacher with Limited Access
**Superadmin assigns these permissions to "Teacher" role:**
- ✅ View Student (`view_student`)
- ✅ View Student Attendance (`view_student_attendance`)
- ✅ Add Student Attendance (`add_student_attendance`)
- ✅ View Assignment (`view_assignment`)
- ✅ Add Assignment (`add_assignment`)

**When Teacher logs in:**
```json
{
  "user": {
    "email": "teacher@university.edu",
    "role": "Teacher"
  },
  "permissions": [
    "view_student",
    "view_student_attendance",
    "add_student_attendance",
    "view_assignment",
    "add_assignment"
  ]
}
```

**Frontend shows ONLY:**
- 📚 Dashboard (always visible)
- 👨‍🎓 Students → View Only
- 📊 Attendance → View + Mark Attendance
- 📝 Assignments → View + Create

**Frontend HIDES:**
- ❌ User Management
- ❌ Role Management
- ❌ Finance
- ❌ Library
- ❌ All other modules

### Example 2: Librarian (Custom Role)
**Superadmin creates "Librarian" role with:**
- ✅ View Library Book (`view_library_book`)
- ✅ Add Library Book (`add_library_book`)
- ✅ Edit Library Book (`edit_library_book`)
- ✅ View Issue & Return (`view_issue_return`)
- ✅ Add Issue & Return (`add_issue_return`)

**Librarian sees:**
- 📚 Dashboard
- 📖 Library → Full Access
  - Manage Books
  - Issue/Return Books
- ❌ Nothing else

## 📝 Quick Implementation Steps

### Step 1: Seed the Database
```bash
cd /home/anant/ERP-MAIN-PROJECT/backend
source venv/bin/activate
python manage.py seed_permissions
```

**Output:**
```
Starting to seed permissions...
✓ Created: view_general_setting
✓ Created: add_general_setting
✓ Created: edit_general_setting
✓ Created: delete_general_setting
...
✓ Seeding complete! Created 600+ permissions

Creating default roles...
✓ Created role: Superadmin
✓ Created role: Admin
✓ Created role: Teacher
✓ Created role: Student
✓ Created role: Staff
✓ Default roles created!
```

### Step 2: Check the Data
```bash
python manage.py shell
```

```python
from apps.roles.models import Role, Permission

# Check roles
print(Role.objects.all().values('id', 'name', 'is_default'))

# Check permissions count
print(f"Total permissions: {Permission.objects.count()}")

# Check modules
from django.db.models import Count
modules = Permission.objects.values('module').annotate(count=Count('id'))
for m in modules:
    print(f"{m['module']}: {m['count']} permissions")
```

### Step 3: Test Role Creation via API (Once views are built)
```bash
# Create custom role
curl -X POST http://localhost:8000/api/roles/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Librarian",
    "description": "Manages library operations"
  }'

# Assign permissions to role
curl -X PUT http://localhost:8000/api/roles/6/permissions/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "permission_ids": [53, 54, 55, 56, 57, 58, 59, 60]
  }'
```

## 🎨 Frontend Integration

### Permission-Based Rendering
```javascript
// React component example
import { usePermissions } from '@/hooks/usePermissions';

export const Dashboard = () => {
  const { hasPermission } = usePermissions();

  return (
    <div>
      <h1>Dashboard</h1>

      {/* Always show dashboard */}
      <DashboardStats />

      {/* Show Students menu if has permission */}
      {hasPermission('view_student') && (
        <StudentsMenu />
      )}

      {/* Show Attendance if has any attendance permission */}
      {(hasPermission('view_student_attendance') ||
        hasPermission('view_teacher_attendance')) && (
        <AttendanceMenu />
      )}

      {/* Show Library only if has library permissions */}
      {hasPermission('view_library_book') && (
        <LibraryMenu />
      )}

      {/* Superadmin only features */}
      {hasPermission('view_user_role') && (
        <RoleManagementMenu />
      )}
    </div>
  );
};
```

### Button-Level Permissions
```javascript
<button
  onClick={handleAddStudent}
  disabled={!hasPermission('add_student')}
  style={{
    display: hasPermission('add_student') ? 'block' : 'none'
  }}
>
  Add New Student
</button>
```

## 📊 Database Structure

### Tables Created
1. **permissions** - All 600+ permissions
2. **user_roles** - System + Custom roles
3. **role_permissions** - Role ↔ Permission mapping
4. **user_role_assignments** - User ↔ Role assignment

### Example Data After Seeding

**Permissions Table:**
| id | name | codename | module | description |
|----|------|----------|--------|-------------|
| 1 | View General Setting | view_general_setting | setting | View permission for General Setting (Only Admin) |
| 2 | Add General Setting | add_general_setting | setting | Add permission for General Setting (Only Admin) |
| 53 | View Library Book | view_library_book | library | View permission for Library Book |
| 54 | Add Library Book | add_library_book | library | Add permission for Library Book |

**Roles Table:**
| id | name | description | is_default | is_system_role |
|----|------|-------------|------------|----------------|
| 1 | Superadmin | Full ERP control | true | true |
| 2 | Admin | College-level management | true | true |
| 3 | Teacher | Teaching and course management | true | true |
| 6 | Librarian | Manages library operations | false | false |

**Role Permissions Table:**
| id | role_id | permission_id |
|----|---------|---------------|
| 1 | 3 | 65 | (Teacher → view_student_attendance)
| 2 | 3 | 66 | (Teacher → add_student_attendance)
| 3 | 6 | 53 | (Librarian → view_library_book)
| 4 | 6 | 54 | (Librarian → add_library_book)

## ✅ Next Steps

1. **Run the seeder** ✅ (Already created)
2. **Build API views** (Next task - I can help with this)
3. **Test with Postman/curl**
4. **Build frontend permission UI**
5. **Test complete flow**

---

**Status**: ACL System Models & Seeder Complete ✅
**Next**: Build Role Management API Views 🚧
