from django.db import models
from django.contrib.auth.models import AbstractUser

from PIL import Image


# Create your models here.
class CustomUser(AbstractUser):
    CAMPUSES = [
        ("kumasi", "Kumasi"),
        ("mampong", "Mampong"),
    ]

    campus = models.CharField(max_length=10, choices=CAMPUSES)
    bio = models.TextField(blank=True, null=True)
    is_staff_member = models.BooleanField(default=False)
    profile_pic = models.ImageField(
        verbose_name="Profile Picture",
        upload_to="users_profile_pics",
        default="user_profile.png",
    )

    def save(self, *args, **kwargs):
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.profile_pic.path)
        return super(CustomUser, self).save(*args, **kwargs)
