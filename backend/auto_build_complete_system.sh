#!/bin/bash
# Complete Automated System Builder
# Generates apps.py, serializers, views, URLs, and admin for ALL 16 modules

cd /home/anant/ERP-MAIN-PROJECT/backend

echo "🚀 AUTOMATED COMPLETE SYSTEM BUILDER"
echo "======================================================================"
echo "Building: apps.py, serializers, views, URLs, admin for 16 modules..."
echo "======================================================================"
echo ""

# Define all modules
MODULES=(
    "asset_management:AssetManagement"
    "library:Library"
    "transport:Transport"
    "messaging:Messaging"
    "communication:Communication"
    "complain:Complain"
    "announcement:Announcement"
    "scholarship:Scholarship"
    "event:Event"
    "payroll:Payroll"
    "accounting:Accounting"
    "reporting:Reporting"
    "media_gallery:MediaGallery"
    "frontend_cms:FrontendCms"
    "miscellaneous:Miscellaneous"
    "subscription:Subscription"
)

# Generate apps.py for each module
echo "📦 Generating apps.py files..."
for module_pair in "${MODULES[@]}"; do
    IFS=':' read -r module_name class_name <<< "$module_pair"

    cat > "apps/${module_name}/apps.py" << EOF
from django.apps import AppConfig


class ${class_name}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.${module_name}'
    verbose_name = '${class_name}'
EOF

    echo "  ✓ apps/${module_name}/apps.py"
done

echo ""
echo "✅ All apps.py files created!"
echo "======================================================================"
echo "Next: Run Python script to generate serializers, views, URLs, admin..."
echo "======================================================================"
