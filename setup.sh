#!/bin/bash

# University ERP Setup Script
# This script helps you set up the development environment

set -e  # Exit on error

echo "🎓 University ERP System - Setup Script"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if Python 3.11+ is installed
echo "Checking Python version..."
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD=python3.11
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if (( $(echo "$PYTHON_VERSION < 3.11" | bc -l) )); then
        print_warning "Python 3.11+ recommended, but found $PYTHON_VERSION"
    fi
else
    print_error "Python 3 not found. Please install Python 3.11+"
    exit 1
fi
print_success "Python found: $PYTHON_CMD"

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    cd backend
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
    cd ..
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source backend/venv/bin/activate
print_success "Virtual environment activated"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
cd backend
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements/dev.txt
print_success "Dependencies installed"
cd ..

# Copy .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo ""
    echo "Creating .env file..."
    cp backend/.env.example backend/.env
    print_success ".env file created"
    print_warning "Please edit backend/.env with your database credentials"
fi

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p backend/logs backend/staticfiles backend/media database_dumps
print_success "Directories created"

# Check for database dumps
echo ""
echo "Checking for database dumps..."
if [ -f "$HOME/Downloads/Erp_Database" ]; then
    cp "$HOME/Downloads/Erp_Database" database_dumps/
    print_success "Found Erp_Database file"
fi
if [ -f "$HOME/Downloads/Erp_Databaseplain" ]; then
    cp "$HOME/Downloads/Erp_Databaseplain" database_dumps/
    print_success "Found Erp_Databaseplain file"
fi

# Check if Docker is installed
echo ""
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    print_success "Docker and Docker Compose found"

    echo ""
    echo "Do you want to start Docker containers? (y/n)"
    read -r START_DOCKER

    if [ "$START_DOCKER" = "y" ]; then
        echo ""
        echo "Starting Docker containers..."
        docker-compose up -d postgres redis

        echo "Waiting for PostgreSQL to be ready..."
        sleep 10

        # Check if database dump exists
        if [ -f "database_dumps/Erp_Databaseplain" ]; then
            echo ""
            echo "Do you want to restore the database? (y/n)"
            read -r RESTORE_DB

            if [ "$RESTORE_DB" = "y" ]; then
                echo "Restoring database..."
                docker-compose exec -T postgres psql -U erp_user -d erp_university < database_dumps/Erp_Databaseplain
                print_success "Database restored"
            fi
        fi
    fi
else
    print_warning "Docker not found. You'll need to set up PostgreSQL and Redis manually"
fi

echo ""
echo "========================================="
print_success "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your database credentials"
echo "2. Run migrations: cd backend && python manage.py migrate"
echo "3. Create superuser: python manage.py createsuperuser"
echo "4. Start server: python manage.py runserver"
echo ""
echo "For detailed instructions, see SETUP_INSTRUCTIONS.md"
echo ""
