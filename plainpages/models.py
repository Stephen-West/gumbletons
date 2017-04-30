from django.db import models

# Create your models here.

class PlainPage(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    template = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        return self.name
