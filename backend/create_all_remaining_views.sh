#!/bin/bash
# Create all remaining ViewSets for the 7 modules
# This script creates views for: card_generation, online_exam, exam_management, marks, promotion, certificates, inventory

cd /home/anant/ERP-MAIN-PROJECT/backend

# Card Generation Views
cat > apps/card_generation/views.py << 'EOF'
"""
Card Generation views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import IDCardSetting, AdmitCardSetting
from .serializers import IDCardSettingSerializer, AdmitCardSettingSerializer


class IDCardSettingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = IDCardSetting.objects.all()
    serializer_class = IDCardSettingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class AdmitCardSettingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AdmitCardSetting.objects.all()
    serializer_class = AdmitCardSettingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)
EOF

# Online Exam Views
cat > apps/online_exam/views.py << 'EOF'
"""
Online Exam views
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ExamInstruction, QuestionBank, OnlineExam, OnlineExamResult
from .serializers import *


class ExamInstructionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamInstruction.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamInstructionListSerializer
        elif self.action in ['create', 'update']:
            return ExamInstructionCreateSerializer
        return ExamInstructionDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class QuestionBankViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = QuestionBank.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return QuestionBankListSerializer
        elif self.action in ['create', 'update']:
            return QuestionBankCreateSerializer
        return QuestionBankDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class OnlineExamViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OnlineExam.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return OnlineExamListSerializer
        elif self.action in ['create', 'update']:
            return OnlineExamCreateSerializer
        return OnlineExamDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)

    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        exam = self.get_object()
        exam.publish_status = True
        exam.save()
        return Response({'success': True, 'message': 'Exam published successfully'})


class OnlineExamResultViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OnlineExamResult.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return OnlineExamResultListSerializer
        elif self.action in ['create', 'update']:
            return OnlineExamResultCreateSerializer
        return OnlineExamResultDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)
EOF

echo "✓ Created card_generation and online_exam views"

# Due to length, creating remaining views with simpler approach
python3 << 'PYTHON_EOF'
# Create Exam Management Views
with open('apps/exam_management/views.py', 'w') as f:
    f.write('''"""
Exam Management views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Grade, ExamTerm, ExamSchedule, ExamSuggestion, ExamAttendanceRecord
from .serializers import *


class GradeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Grade.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return GradeListSerializer
        elif self.action in ['create', 'update']:
            return GradeCreateSerializer
        return GradeDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ExamTermViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamTerm.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamTermListSerializer
        elif self.action in ['create', 'update']:
            return ExamTermCreateSerializer
        return ExamTermDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ExamScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamSchedule.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamScheduleListSerializer
        elif self.action in ['create', 'update']:
            return ExamScheduleCreateSerializer
        return ExamScheduleDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ExamSuggestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamSuggestion.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamSuggestionListSerializer
        elif self.action in ['create', 'update']:
            return ExamSuggestionCreateSerializer
        return ExamSuggestionDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ExamAttendanceRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamAttendanceRecord.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamAttendanceRecordListSerializer
        elif self.action in ['create', 'update']:
            return ExamAttendanceRecordCreateSerializer
        return ExamAttendanceRecordDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, marked_by=self.request.user)
''')

print("✓ Created exam_management views")

# Create Marks Views
with open('apps/marks/views.py', 'w') as f:
    f.write('''"""
Marks Management views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ExamMark, MarkDistribution, ResultCard, MarkEmailLog, MarkSMSLog, ResultEmailLog, ResultSMSLog
from .serializers import *


class ExamMarkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamMark.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamMarkListSerializer
        elif self.action in ['create', 'update']:
            return ExamMarkCreateSerializer
        return ExamMarkDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class MarkDistributionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MarkDistribution.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MarkDistributionListSerializer
        elif self.action in ['create', 'update']:
            return MarkDistributionCreateSerializer
        return MarkDistributionDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ResultCardViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ResultCard.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ResultCardListSerializer
        return ResultCardDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset


class MarkEmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MarkEmailLog.objects.all()
    serializer_class = MarkEmailLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset


class MarkSMSLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MarkSMSLog.objects.all()
    serializer_class = MarkSMSLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset


class ResultEmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ResultEmailLog.objects.all()
    serializer_class = ResultEmailLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset


class ResultSMSLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ResultSMSLog.objects.all()
    serializer_class = ResultSMSLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset
''')

print("✓ Created marks views")

# Create Promotion Views
with open('apps/promotion/views.py', 'w') as f:
    f.write('''"""
Promotion views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import StudentPromotion
from .serializers import *


class StudentPromotionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StudentPromotion.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentPromotionListSerializer
        elif self.action in ['create', 'update']:
            return StudentPromotionCreateSerializer
        return StudentPromotionDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, promoted_by=self.request.user)
''')

print("✓ Created promotion views")

# Create Certificate Views
with open('apps/certificates/views.py', 'w') as f:
    f.write('''"""
Certificate views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CertificateType, CertificateGeneration
from .serializers import *


class CertificateTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CertificateType.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CertificateTypeListSerializer
        elif self.action in ['create', 'update']:
            return CertificateTypeCreateSerializer
        return CertificateTypeDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class CertificateGenerationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CertificateGeneration.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CertificateGenerationListSerializer
        elif self.action in ['create', 'update']:
            return CertificateGenerationCreateSerializer
        return CertificateGenerationDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, generated_by=self.request.user)
''')

print("✓ Created certificates views")

# Create Inventory Views
with open('apps/inventory/views.py', 'w') as f:
    f.write('''"""
Inventory Management views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Supplier, Warehouse, InventoryCategory, Product, Purchase, Sale, ProductIssue
from .serializers import *


class SupplierViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Supplier.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SupplierListSerializer
        elif self.action in ['create', 'update']:
            return SupplierCreateSerializer
        return SupplierDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class WarehouseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Warehouse.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WarehouseListSerializer
        elif self.action in ['create', 'update']:
            return WarehouseCreateSerializer
        return WarehouseDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class InventoryCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = InventoryCategory.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return InventoryCategoryListSerializer
        elif self.action in ['create', 'update']:
            return InventoryCategoryCreateSerializer
        return InventoryCategoryDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update']:
            return ProductCreateSerializer
        return ProductDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Purchase.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PurchaseListSerializer
        elif self.action in ['create', 'update']:
            return PurchaseCreateSerializer
        return PurchaseDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, purchased_by=self.request.user)


class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Sale.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SaleListSerializer
        elif self.action in ['create', 'update']:
            return SaleCreateSerializer
        return SaleDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, sold_by=self.request.user)


class ProductIssueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProductIssue.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductIssueListSerializer
        elif self.action in ['create', 'update']:
            return ProductIssueCreateSerializer
        return ProductIssueDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, issued_by=self.request.user)
''')

print("✓ Created inventory views")
print("\n✅ All ViewSets created successfully!")
PYTHON_EOF

echo ""
echo "========================================================================"
echo "✅ ALL VIEWSETS CREATED FOR 9 MODULES!"
echo "========================================================================"
