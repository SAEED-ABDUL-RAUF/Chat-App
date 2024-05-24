from django.contrib import admin
from .models import GroupMessage, Group

# Register your models here.

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}



admin.site.register(GroupMessage)