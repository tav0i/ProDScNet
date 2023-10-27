from django.db import models

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name='Title')
    image = models.ImageField(upload_to='images/', verbose_name="Image", null=True, blank=True)
    description = models.TextField(null=True,  blank=True, verbose_name='Description')

    def __str__(self):
        register = "Title: " +self.title + " - " + "Description: " + self.description
        return register

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()