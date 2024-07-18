from django.db import models
from django.utils.text import slugify

from PIL import Image
from users.models import CustomUser

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(
        CustomUser, related_name="groups_members", blank=True
    )
    slug = models.SlugField(unique=True, null=False, default="", max_length=255)
    date_created = models.DateField(auto_now_add=True)
    profile_pic = models.ImageField(
        default="group_profile.png", upload_to="groups_profile_pics"
    )
    is_private = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        img = Image.open(self.profile_pic)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.profile_pic.path)
        super(Group, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Chat Group"
        verbose_name_plural = "Chat Groups"

    def __str__(self):
        return self.name


class GroupMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="messages", blank=True, null=True
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="group_chat_files", blank=True, null=True)

    def __str__(self):
        return f"{self.sender} message to {self.group.name}"


class PrivateMessage(models.Model):
    sender = models.ForeignKey(
        CustomUser, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        CustomUser, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="private_chat_files", blank=True, null=True)

    def __str__(self):
        return f"{self.sender} message to {self.receiver}"
