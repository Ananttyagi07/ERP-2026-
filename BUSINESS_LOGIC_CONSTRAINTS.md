# Business Logic Constraints & Data Validation

**Your Question:** "If there's no class, there should be no students. If there's no teacher, no classes should be created."

**Answer:** YES! You need **business logic constraints**. Here's the best way to implement them.

---

## 🎯 THE CONSTRAINTS YOU NEED

### Your Business Rules:

```
1. ❌ No Class → No Students
   "Students cannot be created without a class"

2. ❌ No Teacher → No Class
   "Classes cannot be created without a teacher"

3. ❌ No Subject → No Class
   "Classes need subjects to be created"

4. ❌ No Department → No Teacher
   "Teachers must belong to a department"

5. ❌ Deleted Class → Students become orphaned
   "Deleting a class should handle existing students"

... and many more business rules!
```

---

## 🏗️ IMPLEMENTATION STRATEGIES

### ⭐ **Best Approach: Multi-Layer Validation**

```
┌─────────────────────────────────────┐
│  Layer 1: Database Constraints      │ ← ForeignKey, NOT NULL
├─────────────────────────────────────┤
│  Layer 2: Model Validation          │ ← clean() method
├─────────────────────────────────────┤
│  Layer 3: Serializer Validation     │ ← validate() method
├─────────────────────────────────────┤
│  Layer 4: View Business Logic       │ ← perform_create()
├─────────────────────────────────────┤
│  Layer 5: Custom Permissions        │ ← Permission classes
└─────────────────────────────────────┘
```

Let me show you each layer with examples from YOUR project!

---

## 1️⃣ **LAYER 1: Database Constraints (Automatic)**

### What You Already Have ✅

```python
# apps/students/models.py
class Student(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_class = models.ForeignKey(
        'academic.SchoolClass',
        on_delete=models.CASCADE,  # ← If class deleted, student deleted
        related_name='students'
    )
    section = models.ForeignKey(
        'academic.ClassSection',
        on_delete=models.SET_NULL,  # ← If section deleted, student remains
        null=True,
        blank=True
    )
```

**This already prevents:**
- ✅ Creating a student without a class (database enforces it)
- ✅ Student existing after class is deleted (CASCADE)

**Database-level protection!** ✅

---

## 2️⃣ **LAYER 2: Model Validation (Business Rules)**

### Add `clean()` Method to Models

```python
# apps/students/models.py
from django.core.exceptions import ValidationError

class Student(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.SET_NULL, null=True)

    def clean(self):
        """Validate business rules before saving"""
        super().clean()

        # Rule 1: Student must have a class
        if not self.school_class:
            raise ValidationError({
                'school_class': 'Student must be assigned to a class'
            })

        # Rule 2: Section must belong to the class
        if self.section and self.section.school_class != self.school_class:
            raise ValidationError({
                'section': f'Section {self.section.name} does not belong to class {self.school_class.name}'
            })

        # Rule 3: Check class capacity (example)
        if self.school_class.max_students:
            current_count = Student.objects.filter(
                school_class=self.school_class,
                is_deleted=False
            ).count()

            if current_count >= self.school_class.max_students:
                raise ValidationError({
                    'school_class': f'Class {self.school_class.name} is full (max: {self.school_class.max_students})'
                })

        # Rule 4: Admission date cannot be in future
        from datetime import date
        if self.admission_date and self.admission_date > date.today():
            raise ValidationError({
                'admission_date': 'Admission date cannot be in the future'
            })

    def save(self, *args, **kwargs):
        """Call clean() before saving"""
        self.full_clean()  # This calls clean()
        super().save(*args, **kwargs)
```

---

### More Examples: SchoolClass Validation

```python
# apps/academic/models.py
class SchoolClass(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    name = models.CharField(max_length=100)
    class_teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    subjects = models.ManyToManyField('academic.Subject')

    def clean(self):
        """Validate class business rules"""
        super().clean()

        # Rule 1: Class must have at least one subject
        if self.pk:  # Only check for existing classes
            if not self.subjects.exists():
                raise ValidationError({
                    'subjects': 'Class must have at least one subject assigned'
                })

        # Rule 2: Class teacher must be from same college
        if self.class_teacher and self.class_teacher.college != self.college:
            raise ValidationError({
                'class_teacher': 'Class teacher must be from the same college'
            })

        # Rule 3: Class name must be unique within college
        existing = SchoolClass.objects.filter(
            college=self.college,
            name=self.name,
            is_deleted=False
        ).exclude(pk=self.pk)

        if existing.exists():
            raise ValidationError({
                'name': f'Class {self.name} already exists in this college'
            })
```

---

## 3️⃣ **LAYER 3: Serializer Validation (API-Level)**

### Add Validation to Serializers

```python
# apps/students/serializers.py
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Student
from apps.academic.models import SchoolClass, ClassSection

class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate_school_class(self, value):
        """Validate class exists and is active"""
        if not value:
            raise serializers.ValidationError("Class is required")

        if value.is_deleted:
            raise serializers.ValidationError("Cannot assign student to a deleted class")

        # Check if class has capacity
        if value.max_students:
            current_count = Student.objects.filter(
                school_class=value,
                is_deleted=False
            ).count()

            if current_count >= value.max_students:
                raise serializers.ValidationError(
                    f"Class {value.name} is full (max: {value.max_students} students)"
                )

        return value

    def validate_section(self, value):
        """Validate section exists and belongs to class"""
        if value and value.is_deleted:
            raise serializers.ValidationError("Cannot assign student to a deleted section")

        return value

    def validate(self, attrs):
        """Cross-field validation"""
        school_class = attrs.get('school_class')
        section = attrs.get('section')

        # Validate section belongs to class
        if section and school_class:
            if section.school_class != school_class:
                raise serializers.ValidationError({
                    'section': f'Section {section.name} does not belong to class {school_class.name}'
                })

        # Validate student doesn't already exist
        user = attrs.get('user')
        if user:
            existing = Student.objects.filter(user=user, is_deleted=False)
            if existing.exists():
                raise serializers.ValidationError({
                    'user': 'This user is already registered as a student'
                })

        return attrs

    def create(self, validated_data):
        """Create with additional checks"""
        try:
            instance = super().create(validated_data)
            return instance
        except DjangoValidationError as e:
            # Convert Django validation errors to DRF errors
            raise serializers.ValidationError(e.message_dict)
```

---

### SchoolClass Serializer Example

```python
# apps/academic/serializers.py
class SchoolClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = '__all__'

    def validate_class_teacher(self, value):
        """Validate teacher exists and is available"""
        if value:
            # Check teacher is active
            if value.is_deleted:
                raise serializers.ValidationError("Cannot assign deleted teacher")

            # Check teacher doesn't have too many classes
            current_classes = SchoolClass.objects.filter(
                class_teacher=value,
                is_deleted=False
            ).count()

            max_classes = 3  # Business rule: teacher can handle max 3 classes
            if current_classes >= max_classes:
                raise serializers.ValidationError(
                    f"Teacher {value.user.get_full_name()} already handles {current_classes} classes (max: {max_classes})"
                )

        return value

    def validate(self, attrs):
        """Validate class creation requirements"""
        # Rule: Must have subjects (checked after creation via M2M)
        # This is handled in the view's perform_create

        return attrs
```

---

## 4️⃣ **LAYER 4: View Business Logic**

### Add Pre-Create Checks in ViewSets

```python
# apps/students/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()

    def perform_create(self, serializer):
        """Additional business logic before creating student"""
        # Get the class
        school_class = serializer.validated_data.get('school_class')

        # Pre-flight checks
        self._validate_prerequisites(school_class)

        # Create student
        with transaction.atomic():
            student = serializer.save()

            # Post-creation actions
            self._send_welcome_email(student)
            self._create_student_credentials(student)
            self._assign_default_subjects(student)

        return student

    def _validate_prerequisites(self, school_class):
        """Validate all prerequisites exist"""
        # Check 1: Class must exist
        if not school_class:
            raise serializers.ValidationError("Class is required")

        # Check 2: Class must have teacher
        if not school_class.class_teacher:
            raise serializers.ValidationError(
                f"Class {school_class.name} has no teacher assigned. "
                "Please assign a teacher before adding students."
            )

        # Check 3: Class must have subjects
        if not school_class.subjects.exists():
            raise serializers.ValidationError(
                f"Class {school_class.name} has no subjects assigned. "
                "Please assign subjects before adding students."
            )

        # Check 4: Class must have sections
        if not school_class.sections.exists():
            raise serializers.ValidationError(
                f"Class {school_class.name} has no sections. "
                "Please create sections before adding students."
            )

    def _send_welcome_email(self, student):
        """Send welcome email to student"""
        # Implementation here
        pass

    def _create_student_credentials(self, student):
        """Create login credentials for student"""
        # Implementation here
        pass

    def _assign_default_subjects(self, student):
        """Auto-assign class subjects to student"""
        # Implementation here
        pass
```

---

### SchoolClass ViewSet Example

```python
# apps/academic/views.py
class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all()

    def perform_create(self, serializer):
        """Create class with validations"""
        # Validate prerequisites
        college = serializer.validated_data.get('college')

        # Check: College must have teachers
        from apps.teachers.models import Teacher
        if not Teacher.objects.filter(college=college, is_deleted=False).exists():
            raise serializers.ValidationError(
                "Cannot create class. College has no teachers. "
                "Please add teachers first."
            )

        # Check: College must have subjects
        from apps.academic.models import Subject
        if not Subject.objects.filter(college=college, is_deleted=False).exists():
            raise serializers.ValidationError(
                "Cannot create class. College has no subjects. "
                "Please add subjects first."
            )

        # Create class
        with transaction.atomic():
            school_class = serializer.save()

            # Auto-create default section
            from apps.academic.models import ClassSection
            ClassSection.objects.create(
                school_class=school_class,
                name='A',
                college=college
            )

        return school_class

    def perform_destroy(self, instance):
        """Soft delete class and handle students"""
        # Check if class has students
        student_count = instance.students.filter(is_deleted=False).count()

        if student_count > 0:
            raise serializers.ValidationError(
                f"Cannot delete class {instance.name}. "
                f"It has {student_count} active students. "
                "Please transfer students to another class first."
            )

        # Soft delete
        instance.is_deleted = True
        instance.save()
```

---

## 5️⃣ **LAYER 5: Custom Permissions**

### Create Business-Logic Permissions

```python
# apps/core/permissions.py
from rest_framework.permissions import BasePermission
from apps.academic.models import SchoolClass
from apps.teachers.models import Teacher

class CanCreateStudent(BasePermission):
    """
    Permission: Can only create student if prerequisites exist
    """
    message = "Cannot create students. Prerequisites not met."

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True  # Only check on create

        # Get college from request data
        college_id = request.data.get('college')
        if not college_id:
            return False

        # Check prerequisites
        # 1. College must have classes
        classes_exist = SchoolClass.objects.filter(
            college_id=college_id,
            is_deleted=False
        ).exists()

        if not classes_exist:
            self.message = "Cannot create students. No classes exist in this college. Please create classes first."
            return False

        # 2. College must have teachers
        teachers_exist = Teacher.objects.filter(
            college_id=college_id,
            is_deleted=False
        ).exists()

        if not teachers_exist:
            self.message = "Cannot create students. No teachers exist in this college. Please add teachers first."
            return False

        return True


class CanCreateClass(BasePermission):
    """
    Permission: Can only create class if teachers and subjects exist
    """
    message = "Cannot create class. Prerequisites not met."

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True

        college_id = request.data.get('college')
        if not college_id:
            return False

        # Check: Teachers must exist
        from apps.teachers.models import Teacher
        if not Teacher.objects.filter(college_id=college_id, is_deleted=False).exists():
            self.message = "Cannot create class. No teachers in college. Add teachers first."
            return False

        # Check: Subjects must exist
        from apps.academic.models import Subject
        if not Subject.objects.filter(college_id=college_id, is_deleted=False).exists():
            self.message = "Cannot create class. No subjects in college. Add subjects first."
            return False

        return True
```

### Use in ViewSets

```python
# apps/students/views.py
from apps.core.permissions import CanCreateStudent

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CanCreateStudent]
    # Now student creation is blocked until prerequisites exist!
```

---

## 🔄 **BETTER APPROACH: Dependency Chain**

### Create Setup Order Enforcement

```python
# apps/core/validators.py
from django.core.exceptions import ValidationError

class DependencyValidator:
    """
    Validates that prerequisites exist in the correct order

    Setup Order:
    1. College
    2. Departments
    3. Subjects
    4. Teachers
    5. Classes
    6. Sections
    7. Students
    """

    DEPENDENCY_CHAIN = {
        'Student': ['SchoolClass', 'ClassSection'],
        'SchoolClass': ['Subject', 'Teacher'],
        'Teacher': ['Department'],
        'ClassSection': ['SchoolClass'],
        'Attendance': ['Student', 'SchoolClass'],
        'Exam': ['SchoolClass', 'Subject'],
        'Mark': ['Exam', 'Student']
    }

    @classmethod
    def validate_dependencies(cls, model_name, college):
        """Check if all dependencies exist"""
        missing = []

        if model_name not in cls.DEPENDENCY_CHAIN:
            return  # No dependencies

        dependencies = cls.DEPENDENCY_CHAIN[model_name]

        for dep in dependencies:
            if not cls._check_exists(dep, college):
                missing.append(dep)

        if missing:
            raise ValidationError(
                f"Cannot create {model_name}. Missing: {', '.join(missing)}. "
                f"Please create them first."
            )

    @staticmethod
    def _check_exists(model_name, college):
        """Check if model instances exist for college"""
        from django.apps import apps

        try:
            model = apps.get_model(app_label='academic', model_name=model_name)
            return model.objects.filter(college=college, is_deleted=False).exists()
        except:
            return True  # If model doesn't exist, assume no dependency
```

### Use in ViewSets

```python
# apps/students/views.py
from apps.core.validators import DependencyValidator

class StudentViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        college = serializer.validated_data.get('college')

        # Validate dependencies
        DependencyValidator.validate_dependencies('Student', college)

        # If validation passes, create student
        return serializer.save()
```

---

## 📋 **COMPLETE IMPLEMENTATION EXAMPLE**

### File Structure

```
apps/
├── core/
│   ├── validators.py          # Dependency validation
│   ├── permissions.py         # Business logic permissions
│   └── exceptions.py          # Custom exceptions
│
├── students/
│   ├── models.py              # Model with clean()
│   ├── serializers.py         # Serializer validation
│   ├── views.py               # View business logic
│   └── permissions.py         # Student-specific permissions
│
└── academic/
    ├── models.py              # Class model with clean()
    ├── serializers.py         # Class validation
    └── views.py               # Class creation logic
```

---

## 🎯 **RECOMMENDED SETUP ORDER**

### Create a Setup Wizard

```python
# apps/core/setup_wizard.py
class CollegeSetupWizard:
    """
    Guides college setup in correct order
    Prevents creating things out of order
    """

    STEPS = [
        {
            'step': 1,
            'name': 'Create Departments',
            'model': 'Department',
            'required': True,
            'min_count': 1
        },
        {
            'step': 2,
            'name': 'Create Subjects',
            'model': 'Subject',
            'required': True,
            'min_count': 3
        },
        {
            'step': 3,
            'name': 'Add Teachers',
            'model': 'Teacher',
            'required': True,
            'min_count': 1
        },
        {
            'step': 4,
            'name': 'Create Classes',
            'model': 'SchoolClass',
            'required': True,
            'min_count': 1
        },
        {
            'step': 5,
            'name': 'Create Sections',
            'model': 'ClassSection',
            'required': True,
            'min_count': 1
        },
        {
            'step': 6,
            'name': 'Add Students',
            'model': 'Student',
            'required': False,
            'min_count': 0
        }
    ]

    @classmethod
    def get_current_step(cls, college):
        """Determine which step college is on"""
        for step_info in cls.STEPS:
            if not cls._step_completed(step_info, college):
                return step_info

        return None  # All steps complete

    @classmethod
    def _step_completed(cls, step_info, college):
        """Check if step is completed"""
        from django.apps import apps

        model = apps.get_model('academic', step_info['model'])
        count = model.objects.filter(college=college, is_deleted=False).count()

        return count >= step_info['min_count']

    @classmethod
    def can_proceed_to(cls, step_number, college):
        """Check if college can proceed to given step"""
        for step_info in cls.STEPS:
            if step_info['step'] < step_number:
                if not cls._step_completed(step_info, college):
                    return False, f"Complete step {step_info['step']}: {step_info['name']} first"

        return True, "OK"
```

---

## ✅ **FINAL RECOMMENDATIONS**

### What to Implement First:

**Priority 1: Model-Level Validation (1-2 hours)**
```python
# Add clean() methods to:
- Student model
- SchoolClass model
- Teacher model
- Attendance model
```

**Priority 2: Serializer Validation (2-3 hours)**
```python
# Add validate() methods to all serializers
```

**Priority 3: View-Level Checks (2-3 hours)**
```python
# Add perform_create() checks in ViewSets
```

**Priority 4: Custom Permissions (1 hour)**
```python
# Create CanCreateStudent, CanCreateClass permissions
```

**Priority 5: Setup Wizard (Optional - 4 hours)**
```python
# Create guided setup flow
```

---

## 🎯 **SUMMARY**

**Your Question:** "How to prevent creating students without classes?"

**Answer:** Use **multi-layer validation**:

1. ✅ **Database:** ForeignKey constraints (already done)
2. ✅ **Model:** `clean()` method validation
3. ✅ **Serializer:** `validate()` method checks
4. ✅ **View:** `perform_create()` business logic
5. ✅ **Permission:** Custom permission classes

**Best Practice:**
- Start with Model validation
- Add Serializer validation
- Add View-level checks for complex rules
- Use Custom Permissions for role-based prerequisites

**Want me to implement this for your specific models?**
