from django.db import models

# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.title