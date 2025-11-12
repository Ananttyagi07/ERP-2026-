# API Testing Guide - University ERP System

## 🚀 Quick Start

### Step 1: Start the Backend Server

```bash
cd /home/anant/ERP-MAIN-PROJECT/backend

# Activate virtual environment
source venv/bin/activate

# Run migrations (if not done already)
python manage.py makemigrations
python manage.py migrate

# Seed permissions and default roles
python manage.py seed_permissions

# Create a superuser for testing
python manage.py createsuperuser
# Email: admin@university.edu
# Username: admin
# Password: admin123

# Start the development server
python manage.py runserver 0.0.0.0:8000
```

**Server should be running at**: `http://localhost:8000`

---

## 🧪 Testing with cURL

### Test 1: Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@university.edu",
    "password": "admin123"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {...},
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
      "refresh": "random_refresh_token_string"
    },
    "redirect_url": "/superadmin/dashboard"
  }
}
```

**Save the access token** for subsequent requests.

---

### Test 2: Get My Permissions

```bash
# Replace YOUR_ACCESS_TOKEN with the token from login response
export ACCESS_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGci..."

curl -X GET http://localhost:8000/api/auth/my-permissions/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "admin@university.edu",
      "role": "Superadmin",
      "college_id": 1
    },
    "permissions": [
      {
        "id": 1,
        "name": "View General Setting",
        "codename": "view_general_setting",
        "module": "setting"
      }
    ]
  }
}
```

---

### Test 3: List All Roles

```bash
curl -X GET http://localhost:8000/api/roles/roles/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Expected Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Superadmin",
      "description": "Full ERP control",
      "is_default": true,
      "permissions_count": 150,
      "users_count": 1
    }
  ]
}
```

---

### Test 4: Create Custom Role

```bash
curl -X POST http://localhost:8000/api/roles/roles/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Librarian",
    "description": "Manages library operations and book inventory",
    "college_id": 1,
    "is_active": true
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Role created successfully",
  "data": {
    "id": 6,
    "name": "Librarian",
    "description": "Manages library operations and book inventory",
    "college_id": 1,
    "is_active": true
  }
}
```

---

### Test 5: Get All Permissions Grouped by Module

```bash
curl -X GET http://localhost:8000/api/roles/permissions/grouped/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "permissions_by_module": [
      {
        "module": "library",
        "module_name": "Library",
        "permissions": [
          {"id": 53, "name": "View Library Book", "codename": "view_library_book"},
          {"id": 54, "name": "Add Library Book", "codename": "add_library_book"},
          {"id": 55, "name": "Edit Library Book", "codename": "edit_library_book"},
          {"id": 56, "name": "Delete Library Book", "codename": "delete_library_book"}
        ]
      }
    ]
  }
}
```

---

### Test 6: Assign Permissions to Role

Let's assign library-related permissions to the Librarian role we created:

```bash
curl -X PUT http://localhost:8000/api/roles/roles/6/permissions/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "permission_ids": [53, 54, 55, 56, 57, 58, 59, 60]
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "8 permissions assigned to role successfully"
}
```

---

### Test 7: Get Role with Permissions

```bash
curl -X GET http://localhost:8000/api/roles/roles/6/permissions/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "role": {
      "id": 6,
      "name": "Librarian",
      "description": "Manages library operations"
    },
    "permissions_by_module": [
      {
        "module": "library",
        "module_name": "Library",
        "permissions": [
          {
            "id": 53,
            "name": "View Library Book",
            "codename": "view_library_book",
            "is_assigned": true
          },
          {
            "id": 54,
            "name": "Add Library Book",
            "codename": "add_library_book",
            "is_assigned": true
          }
        ]
      }
    ]
  }
}
```

---

### Test 8: Refresh Token

```bash
# Save refresh token from login
export REFRESH_TOKEN="random_refresh_token_string"

curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d "{
    \"refresh_token\": \"$REFRESH_TOKEN\"
  }"
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "tokens": {
      "access": "new_access_token",
      "refresh": "new_refresh_token"
    }
  }
}
```

---

### Test 9: Logout

```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"refresh_token\": \"$REFRESH_TOKEN\"
  }"
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

## 🧪 Testing with Postman

### Setup

1. **Import Collection** (create these requests):
   - POST Login
   - GET My Permissions
   - GET List Roles
   - POST Create Role
   - GET Permissions Grouped
   - PUT Assign Permissions

2. **Set Environment Variables**:
   - `base_url`: `http://localhost:8000/api`
   - `access_token`: (will be set from login response)
   - `refresh_token`: (will be set from login response)

3. **Pre-request Script for Authorization**:
```javascript
pm.request.headers.add({
    key: 'Authorization',
    value: 'Bearer ' + pm.environment.get('access_token')
});
```

4. **Test Script for Login** (save tokens):
```javascript
var jsonData = pm.response.json();
if (jsonData.success) {
    pm.environment.set('access_token', jsonData.data.tokens.access);
    pm.environment.set('refresh_token', jsonData.data.tokens.refresh);
}
```

---

## 🔍 Testing with Browser (Swagger UI)

Django REST Framework provides browsable API:

1. **Navigate to**: `http://localhost:8000/api/`

2. **Login First**:
   - Go to `http://localhost:8000/api/auth/login/`
   - Click "POST" button
   - Enter credentials in JSON format
   - Copy the access token

3. **Authenticate**:
   - Click "Authorize" button (lock icon)
   - Enter: `Bearer YOUR_ACCESS_TOKEN`
   - Click "Authorize"

4. **Test Endpoints**:
   - All endpoints are now accessible
   - Try different HTTP methods (GET, POST, PUT, DELETE)

---

## 📊 API Documentation (Swagger)

The project includes automatic API documentation:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

---

## ✅ Complete Testing Scenario

### Scenario: Create a "Head Teacher" Role with Limited Permissions

```bash
# 1. Login as Superadmin
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@university.edu", "password": "admin123"}' \
  | jq -r '.data.tokens.access' > token.txt

export ACCESS_TOKEN=$(cat token.txt)

# 2. Create "Head Teacher" role
curl -X POST http://localhost:8000/api/roles/roles/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Head Teacher",
    "description": "Senior teacher with additional responsibilities",
    "college_id": 1
  }' | jq

# Response will show role_id (let's say it's 7)

# 3. Get all available permissions
curl -X GET http://localhost:8000/api/roles/permissions/grouped/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  | jq '.data.permissions_by_module[] | select(.module == "student" or .module == "attendance" or .module == "assignment")'

# 4. Assign specific permissions
curl -X PUT http://localhost:8000/api/roles/roles/7/permissions/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "permission_ids": [45, 46, 65, 66, 67, 68, 89, 90, 91, 92]
  }' | jq

# 5. Verify permissions were assigned
curl -X GET http://localhost:8000/api/roles/roles/7/permissions/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  | jq

# 6. Check role in list
curl -X GET http://localhost:8000/api/roles/roles/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  | jq '.results[] | select(.name == "Head Teacher")'
```

---

## 🐛 Common Issues and Solutions

### Issue 1: "Authentication credentials were not provided"
**Solution**: Make sure you're including the Authorization header:
```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Issue 2: "Token has expired"
**Solution**: Use the refresh token endpoint to get a new access token:
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'
```

### Issue 3: "Permission denied"
**Solution**: Check user permissions:
```bash
curl -X GET http://localhost:8000/api/auth/my-permissions/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Issue 4: "Invalid credentials"
**Solution**:
1. Check if superuser exists: `python manage.py createsuperuser`
2. Verify email and password are correct
3. Check if user is active in database

### Issue 5: "No permissions found"
**Solution**: Run the seeder:
```bash
python manage.py seed_permissions
```

---

## 📈 Performance Testing

### Test Token Caching

```bash
# First request (cache miss)
time curl -X GET http://localhost:8000/api/auth/my-permissions/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# Second request (cache hit - should be faster)
time curl -X GET http://localhost:8000/api/auth/my-permissions/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Load Testing with Apache Bench

```bash
# Test login endpoint (100 requests, 10 concurrent)
ab -n 100 -c 10 -p login.json -T application/json \
  http://localhost:8000/api/auth/login/

# Create login.json file:
echo '{"email":"admin@university.edu","password":"admin123"}' > login.json
```

---

## 🎯 Next Steps

After testing these APIs:

1. ✅ **Authentication APIs** - Complete
2. ✅ **Role & Permission APIs** - Complete
3. 🚧 **Superadmin Management APIs** - Next
4. 🚧 **User Management APIs** - Pending
5. 🚧 **Template Management APIs** - Pending
6. 🚧 **Front Office APIs** - Pending
7. 🚧 **HR Management APIs** - Pending
8. 🚧 **Teacher Management APIs** - Pending
9. 🚧 **Leave Management APIs** - Pending
10. 🚧 **Academic Management APIs** - Pending

---

**Last Updated**: 2025-11-07
**Version**: 1.0
