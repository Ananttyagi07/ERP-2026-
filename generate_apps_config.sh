#!/bin/bash

# Generate apps.py for all 16 new modules

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

echo "Generating apps.py for all modules..."

for module_pair in "${MODULES[@]}"; do
    IFS=':' read -r module_name class_name <<< "$module_pair"
    echo "Creating apps.py for ${module_name}..."

    cat > "apps/${module_name}/apps.py" << EOF
from django.apps import AppConfig


class ${class_name}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.${module_name}'
    verbose_name = '${class_name}'
EOF
done

echo "✓ All apps.py files generated successfully!"
