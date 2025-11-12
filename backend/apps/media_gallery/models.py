"""Media Gallery models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Gallery(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Photo galleries/albums"""
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    is_view_on_web = models.BooleanField(default=False)

    class Meta:
        db_table = 'galleries'
        verbose_name_plural = 'galleries'

    def __str__(self):
        return self.title


class GalleryImage(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Images in galleries"""
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'gallery_images'

    def __str__(self):
        return f"{self.gallery.title} - {self.caption}"
