"""
Student Promotion serializers
"""
from rest_framework import serializers
from .models import StudentPromotion


class StudentPromotionListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    from_class_name = serializers.CharField(source='from_class.name', read_only=True)
    to_class_name = serializers.CharField(source='to_class.name', read_only=True)

    class Meta:
        model = StudentPromotion
        fields = [
            'id', 'student_name', 'from_class_name', 'to_class_name',
            'session_from', 'session_to', 'promotion_date'
        ]


class StudentPromotionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPromotion
        fields = [
            'student', 'from_class', 'from_section', 'to_class', 'to_section',
            'session_from', 'session_to', 'note'
        ]


class StudentPromotionDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    from_class_name = serializers.CharField(source='from_class.name', read_only=True)
    from_section_name = serializers.CharField(source='from_section.name', read_only=True)
    to_class_name = serializers.CharField(source='to_class.name', read_only=True)
    to_section_name = serializers.CharField(source='to_section.name', read_only=True)
    promoted_by_name = serializers.CharField(source='promoted_by.get_full_name', read_only=True)

    class Meta:
        model = StudentPromotion
        fields = '__all__'
