from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,  blank=True)
    technology = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # @property TypeError: 'str' object is not callable
    def __str__(self):
        return self.title + ' - by ' + self.user.username