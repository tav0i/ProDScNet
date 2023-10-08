from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )
# Register your models here.
# Create superuser: python manage.py createsuperuser
admin.site.register(Task, TaskAdmin)
