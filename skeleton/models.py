from django.db import models

# Create your models here.

class Compendium(models.Model):
    sequence = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    prefix = models.CharField(max_length=50, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    #group = models.ForeignKey('Group',null=True, blank=True)
    parent = models.ForeignKey('Menu',null=True, blank=True)
    rubric = models.TextField(null=True, blank=True)
    index = models.BooleanField(default=True)
    record_key = models.CharField(max_length=32, null=True, blank=True)
    template = models.CharField(max_length=32, null=True, blank=True)
    indextemplate = models.CharField(max_length=32, null=True, blank=True)
    sort_date = models.CharField(max_length=15, null=True, blank=True)
    private = models.BooleanField(default=False)
    category = models.CharField(max_length=32, null=True, blank=True, help_text= "Distinguishes between db tables")
    volume = models.CharField(max_length=8, null=True, blank=True, help_text= "Volume number only used for books")
    def __str__(self):
        return '{s}: {n}'.format(s=self.sequence, n=self.name)
    class Meta:
        ordering = ['sequence']

class Menu(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    path = models.CharField(max_length=50, null=True, blank=True)
    rubric = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self',null=True, blank=True) 
    def __str__(self):
        return self.title
