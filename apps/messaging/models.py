"""Internal Messaging System models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Message(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Internal messages between users"""
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.get_full_name()} to {self.receiver.get_full_name()}: {self.subject}"
