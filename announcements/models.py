from django.db import models
from users.models import CustomUser


# Create your models here.
class Announcement(models.Model):
    TARGET_CHOICES = [
        ("students", "Students"),
        ("all_users", "All Users"),
        ("staff", "Staff"),
    ]

    title = models.CharField(max_length=255)
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="announcements"
    )
    content = models.TextField()
    target = models.CharField(
        max_length=10,
        choices=TARGET_CHOICES,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} from {self.sender.username}"
