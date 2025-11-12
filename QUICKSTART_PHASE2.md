# Quick Start Guide - Phase 2 Complete System

## 🚀 Fast Track Setup (5 Minutes)

### Step 1: Install Dependencies
```bash
cd /home/anant/ERP-MAIN-PROJECT/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/base.txt
```

### Step 2: Setup Environment
```bash
# Create .env file
cat > .env << 'EOF'
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production
DATABASE_NAME=erp_university
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
EOF
```

### Step 3: Setup Database
```bash
# Create database
createdb erp_university

# Or if you need to create with specific user:
psql -U postgres -c "CREATE DATABASE erp_university;"
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Seed Permissions
```bash
python manage.py seed_permissions
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### Step 7: Start Server
```bash
python manage.py runserver
```

---

## 📊 What You Have Now

### Total System Capacity
- **61 Database Models**
- **349 API Endpoints**
- **28 Django Apps**
- **600+ Permissions**
- **19 Modules** (10 Phase 1 + 9 Phase 2)

### Access URLs
- API: http://localhost:8000/api/
- Swagger Docs: http://localhost:8000/api/docs/
- Admin Panel: http://localhost:8000/admin/

---

## 🎯 Test Your Setup

### 1. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-password"
  }'
```

### 2. Get Your Permissions
```bash
curl -X GET http://localhost:8000/api/auth/my-permissions/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. List Student Types
```bash
curl -X GET http://localhost:8000/api/student-management/types/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📁 Module Overview

### Phase 2 Modules (NEW)
1. **Student Management** - `/api/student-management/`
   - Types, Online Admissions, Activities

2. **Attendance** - `/api/attendance/`
   - Students, Teachers, Employees, Email/SMS Logs

3. **Card Generation** - `/api/card-generation/`
   - ID Card Settings, Admit Card Settings

4. **Online Exam** - `/api/online-exam/`
   - Instructions, Questions, Exams, Results

5. **Exam Management** - `/api/exam-management/`
   - Grades, Terms, Schedules, Suggestions, Attendance

6. **Marks** - `/api/marks/`
   - Marks Entry, Distributions, Results, Notifications

7. **Promotion** - `/api/promotion/`
   - Student Promotions

8. **Certificates** - `/api/certificates/`
   - Certificate Types, Generation

9. **Inventory** - `/api/inventory/`
   - Suppliers, Warehouses, Products, Purchases, Sales, Issues

### Phase 1 Modules (Already Built)
- Authentication, Users, Roles, Colleges
- Superadmin, Templates, Front Office
- HR, Teachers, Leave Management
- Academic, Live Classes, Students, Guardians

---

## 🔧 Common Commands

### Development
```bash
# Run server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Shell
python manage.py shell
```

### Database
```bash
# Reset database (CAUTION: Deletes all data!)
python manage.py flush

# Seed permissions again
python manage.py seed_permissions
```

### Utilities
```bash
# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check

# Show migrations
python manage.py showmigrations
```

---

## 📝 API Endpoint Examples

### Student Management
```bash
# Create Student Type
POST /api/student-management/types/
{
  "name": "Undergraduate",
  "note": "4-year program"
}

# List Online Admissions
GET /api/student-management/online-admissions/?status=Pending

# Approve Admission
POST /api/student-management/online-admissions/1/approve/
```

### Attendance
```bash
# Mark Student Attendance
POST /api/attendance/students/
{
  "student": 1,
  "school_class": 1,
  "section": 1,
  "attendance_date": "2025-01-15",
  "status": "Present"
}

# Get Attendance by Date
GET /api/attendance/students/?date=2025-01-15
```

### Online Exam
```bash
# Create Question
POST /api/online-exam/questions/
{
  "school_class": 1,
  "section": 1,
  "subject": 1,
  "question_type": "Multiple Choice",
  "question_level": "Easy",
  "question": "What is 2+2?",
  "option_a": "3",
  "option_b": "4",
  "option_c": "5",
  "option_d": "6",
  "correct_answer": "4",
  "mark": 1
}

# Publish Exam
POST /api/online-exam/exams/1/publish/
```

### Inventory
```bash
# Create Product
POST /api/inventory/products/
{
  "name": "Notebook A4",
  "category": 1,
  "warehouse": 1,
  "unit": "Piece",
  "unit_price": 2.50,
  "quantity": 100
}

# Record Sale
POST /api/inventory/sales/
{
  "product": 1,
  "warehouse": 1,
  "quantity": 10,
  "unit_price": 2.50,
  "customer_name": "John Doe",
  "invoice_no": "INV-2025-001",
  "sale_date": "2025-01-15"
}
```

---

## ⚠️ Troubleshooting

### Module Not Found Errors
```bash
# Reinstall dependencies
pip install -r requirements/base.txt
```

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Verify database exists
psql -l | grep erp_university
```

### Migration Errors
```bash
# Delete migrations (except __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

### Redis Connection Error
```bash
# Start Redis
sudo service redis-server start

# Or use Docker
docker run -d -p 6379:6379 redis:alpine
```

---

## 🎉 Success Checklist

- [ ] Dependencies installed (pip install)
- [ ] Database created (createdb)
- [ ] .env file configured
- [ ] Migrations run (makemigrations + migrate)
- [ ] Permissions seeded (seed_permissions)
- [ ] Superuser created (createsuperuser)
- [ ] Server running (runserver)
- [ ] Can login via API
- [ ] Can access Swagger docs
- [ ] Can access Admin panel

---

## 📚 Next Steps

1. **Explore APIs**: Visit http://localhost:8000/api/docs/
2. **Create Test Data**: Use admin panel to create classes, sections, students
3. **Test Workflows**: Try online admission → approval → student creation
4. **Frontend Development**: Start building React frontend
5. **Deployment**: Configure for production (Docker, K8s, etc.)

---

## 💡 Pro Tips

1. **Use Swagger**: Interactive API testing at `/api/docs/`
2. **Check Logs**: Watch terminal for errors
3. **Use Django Shell**: `python manage.py shell` for quick tests
4. **Admin Panel**: Great for initial data setup
5. **Pagination**: Add `?page=1&page_size=10` to list endpoints
6. **Filtering**: Use query params like `?status=Pending&class_id=1`

---

## 🔐 Security Reminders

- Change `SECRET_KEY` in production
- Use strong passwords
- Enable HTTPS in production
- Configure CORS properly
- Set `DEBUG=False` in production
- Use environment variables
- Regular backups

---

**Ready to build amazing features!** 🚀

For detailed documentation, see [PHASE_2_BUILD_COMPLETE.md](PHASE_2_BUILD_COMPLETE.md)
