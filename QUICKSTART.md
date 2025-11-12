# 🚀 Quick Start Guide - University ERP System

## Get Running in 5 Minutes!

### Step 1: Restore Your Databases

```bash
# Navigate to project
cd /home/anant/ERP-MAIN-PROJECT

# Create database dump directory
mkdir -p database_dumps

# Copy your PostgreSQL dumps
cp ~/Downloads/Erp_Database database_dumps/
cp ~/Downloads/Erp_Databaseplain database_dumps/
```

### Step 2: Start Docker Services

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Wait for services to start
sleep 10

# Check if running
docker-compose ps
```

### Step 3: Restore Database

```bash
# Option A: Binary dump
docker-compose exec postgres pg_restore -U erp_user -d erp_university -v /database_dumps/Erp_Database

# Option B: Plain text dump (if binary fails)
docker-compose exec -T postgres psql -U erp_user -d erp_university < database_dumps/Erp_Databaseplain
```

### Step 4: Setup Backend

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements/dev.txt
```

### Step 5: Configure Environment

```bash
# Copy environment file
cp .env.example .env

# Edit if needed (defaults should work with Docker)
nano .env
```

Default `.env` values for Docker:
```env
DEBUG=True
SECRET_KEY=your-secret-key-change-later
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=erp_university
DATABASE_USER=erp_user
DATABASE_PASSWORD=erp_password
```

### Step 6: Initialize Database (If needed)

If you're NOT using the restored database:

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Email: admin@test.com
# Password: admin123
```

### Step 7: Start Development Server

```bash
# Start Django
python manage.py runserver

# Server will be available at: http://localhost:8000
```

### Step 8: Test the System

**Check API Documentation:**
```
http://localhost:8000/api/docs/
```

**Test Login (using curl):**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "admin123"
  }'
```

**Test Login (using httpie - prettier):**
```bash
# Install httpie if you don't have it
pip install httpie

# Make request
http POST http://localhost:8000/api/auth/login/ \
  email=admin@test.com \
  password=admin123
```

## 🎯 What You Should See

### Successful Login Response:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "email": "admin@test.com",
      "username": "admin",
      "full_name": "Admin User",
      "college_id": 1,
      "college_name": "Main Campus",
      "is_superuser": true,
      "primary_role": {
        "id": 1,
        "name": "Superadmin",
        "description": "Full ERP control"
      }
    },
    "tokens": {
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh": "c3VwZXJzZWNyZXRyZWZyZXNodG9rZW4..."
    }
  }
}
```

### Then Test Protected Endpoint:
```bash
# Replace YOUR_ACCESS_TOKEN with the token from login response
curl -X GET http://localhost:8000/api/auth/my-permissions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:
```json
{
  "user": {
    "id": 1,
    "email": "admin@test.com",
    "role": "Superadmin",
    "college_id": 1
  },
  "permissions": [
    {"id": 1, "name": "View Dashboard", "codename": "view_dashboard", "module": "dashboard"},
    {"id": 2, "name": "Manage Users", "codename": "manage_users", "module": "users"},
    ...
  ]
}
```

## 🔍 Explore Your Restored Database

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U erp_user -d erp_university

# List all tables
\dt

# Check users
SELECT id, email, username, first_name, last_name, college_id, is_active
FROM users
LIMIT 5;

# Check colleges
SELECT id, name, code, is_active
FROM colleges;

# Check roles
SELECT id, name, description, is_default
FROM user_roles;

# Exit
\q
```

## 📱 Access Points

| Service | URL |
|---------|-----|
| **API Server** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/api/docs/ |
| **API Docs (Redoc)** | http://localhost:8000/api/redoc/ |
| **Django Admin** | http://localhost:8000/admin/ |
| **PostgreSQL** | localhost:5432 |
| **Redis** | localhost:6379 |

## 🛠️ Useful Commands

### Docker Commands
```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f postgres

# Stop all services
docker-compose down

# Restart a service
docker-compose restart backend

# View running containers
docker-compose ps
```

### Django Commands
```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

### Database Commands
```bash
# Backup database
docker-compose exec postgres pg_dump -U erp_user erp_university > backup.sql

# Restore database
docker-compose exec -T postgres psql -U erp_user erp_university < backup.sql

# Connect to database
docker-compose exec postgres psql -U erp_user -d erp_university
```

## 🐛 Common Issues & Solutions

### Issue: "Port 5432 already in use"
```bash
# Check if PostgreSQL is running locally
sudo systemctl status postgresql

# Stop local PostgreSQL
sudo systemctl stop postgresql

# Or change port in docker-compose.yml
ports:
  - "5433:5432"  # Use 5433 instead
```

### Issue: "Database does not exist"
```bash
# Create database manually
docker-compose exec postgres createdb -U erp_user erp_university
```

### Issue: "Permission denied"
```bash
# Fix permissions
chmod +x setup.sh
chmod -R 755 backend/
```

### Issue: "Module not found"
```bash
# Make sure virtual environment is activated
source backend/venv/bin/activate

# Reinstall requirements
pip install -r backend/requirements/dev.txt
```

### Issue: "Migrations not applied"
```bash
# Apply migrations
python manage.py migrate

# If migrations conflict, reset
python manage.py migrate --fake-initial
```

## 📊 Check System Health

```bash
# Check if all services are running
docker-compose ps

# Should show:
# erp_postgres    running   0.0.0.0:5432->5432/tcp
# erp_redis       running   0.0.0.0:6379->6379/tcp

# Check Django server
curl http://localhost:8000/api/docs/

# Check database connection
docker-compose exec postgres pg_isready -U erp_user
```

## 🎓 Next Steps

1. **Explore the Database**
   - Check what tables exist
   - See what data is already there
   - Understand the schema

2. **Test Authentication**
   - Try logging in with existing users
   - Check role and permission loading
   - Verify JWT token generation

3. **Plan API Development**
   - Review `PROJECT_STATUS.md` for roadmap
   - Decide which features to build first
   - Prioritize Superadmin dashboard

4. **Build Frontend (Later)**
   - React app connecting to APIs
   - Role-based routing
   - Permission-based UI rendering

## 📚 Documentation

- **README.md** - Project overview
- **SETUP_INSTRUCTIONS.md** - Detailed setup guide
- **PROJECT_STATUS.md** - What's built, what's next
- **QUICKSTART.md** - This file

## 🤝 Need Help?

If something doesn't work:

1. Check logs: `docker-compose logs -f`
2. Verify environment variables in `.env`
3. Ensure PostgreSQL and Redis are running
4. Check if port 8000 is available
5. Review error messages carefully

---

**You're all set! 🎉**

Your ERP system backend is ready for development and testing!
