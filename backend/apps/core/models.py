"""
Core abstract models for University ERP
"""
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    Abstract base model with automatic timestamp fields
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract base model with soft delete functionality
    """
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        """Soft delete the object"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def restore(self):
        """Restore soft deleted object"""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])


class CollegeIsolatedModel(models.Model):
    """
    Abstract base model for college-level data isolation
    All models extending this will automatically enforce college_id separation
    """
    college = models.ForeignKey(
        'colleges.College',
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        db_index=True
    )

    class Meta:
        abstract = True
