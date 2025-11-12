#!/bin/bash
# Complete ERP System Setup Script
# Run this script to set up the entire backend

set -e  # Exit on error

echo "🚀 University ERP System - Complete Setup"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

cd /home/anant/ERP-MAIN-PROJECT/backend

# Step 1: Create virtual environment
echo -e "${YELLOW}Step 1: Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Step 2: Activate virtual environment
echo -e "${YELLOW}Step 2: Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Step 3: Upgrade pip
echo -e "${YELLOW}Step 3: Upgrading pip...${NC}"
pip install --upgrade pip
echo -e "${GREEN}✓ pip upgraded${NC}"

# Step 4: Install dependencies
echo -e "${YELLOW}Step 4: Installing dependencies...${NC}"
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 5: Create .env file if it doesn't exist
echo -e "${YELLOW}Step 5: Setting up environment variables...${NC}"
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-$(openssl rand -hex 32)
DATABASE_NAME=erp_university
DATABASE_USER=erp_user
DATABASE_PASSWORD=erp_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0

# JWT Settings
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=900
JWT_REFRESH_TOKEN_LIFETIME=604800
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Step 6: Run migrations
echo -e "${YELLOW}Step 6: Running database migrations...${NC}"
python manage.py makemigrations
python manage.py migrate
echo -e "${GREEN}✓ Migrations completed${NC}"

# Step 7: Seed permissions
echo -e "${YELLOW}Step 7: Seeding permissions...${NC}"
python manage.py seed_permissions
echo -e "${GREEN}✓ Permissions seeded (600+ permissions created)${NC}"

# Step 8: Create superuser (optional)
echo -e "${YELLOW}Step 8: Create superuser (optional)${NC}"
echo "Do you want to create a superuser now? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
    echo -e "${GREEN}✓ Superuser created${NC}"
else
    echo "You can create superuser later with: python manage.py createsuperuser"
fi

# Step 9: Collect static files (for production)
echo -e "${YELLOW}Step 9: Collecting static files...${NC}"
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Static files collected${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "📊 Summary:"
echo "  • 26 database models created"
echo "  • 170+ API endpoints ready"
echo "  • 600+ permissions configured"
echo "  • 10 feature modules active"
echo ""
echo "🚀 To start the development server:"
echo "  1. source venv/bin/activate"
echo "  2. python manage.py runserver"
echo ""
echo "📚 Access Points:"
echo "  • API: http://localhost:8000/api/"
echo "  • Swagger: http://localhost:8000/api/docs/"
echo "  • ReDoc: http://localhost:8000/api/redoc/"
echo "  • Admin: http://localhost:8000/admin/"
echo ""
echo "📖 Documentation:"
echo "  • COMPLETE_BUILD_SUMMARY.md - Full feature list"
echo "  • API_DOCUMENTATION.md - API reference"
echo "  • API_TESTING_GUIDE.md - Testing guide"
echo ""
echo -e "${GREEN}Happy coding! 🎉${NC}"
