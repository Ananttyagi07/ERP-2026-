"""Frontend CMS models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class FrontendPage(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Custom frontend pages"""
    LOCATION_CHOICES = [
        ('Header', 'Header'),
        ('Footer', 'Footer'),
        ('Sidebar', 'Sidebar'),
    ]

    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    title = models.CharField(max_length=255)
    url_slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='pages/', null=True, blank=True)

    class Meta:
        db_table = 'frontend_pages'
        unique_together = [['college', 'url_slug']]

    def __str__(self):
        return self.title


class Slider(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Homepage sliders"""
    image = models.ImageField(upload_to='sliders/')
    caption = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'sliders'

    def __str__(self):
        return self.caption or f"Slider {self.id}"


class AboutSchool(TimeStampedModel, CollegeIsolatedModel):
    """About school content (one per college)"""
    content = models.TextField()
    image = models.ImageField(upload_to='about/', null=True, blank=True)

    class Meta:
        db_table = 'about_school'

    def __str__(self):
        return f"About {self.college.name}"
