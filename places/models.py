from django.db import models

# Create your models here.

class Country(models.Model):
    """Country"""
    country = models.CharField(max_length=30)
    def __str__(self):
        return self.country
    class Meta:
        ordering = ['country']

class County(models.Model):
    """County, state or province"""
    county = models.CharField(max_length=30)
    country = models.ForeignKey(Country)
    def __str__(self):
        return "{county}, {country}".format(county=self.county, country=self.country)
    class Meta:
        ordering = ['county']
            
class Place(models.Model):
    """Town or parish referenced in any record"""
    town = models.CharField(max_length=30, null=True, blank=True)
    county = models.ForeignKey(County)
    code = models.CharField(max_length=6)
    detail = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    picture = models.CharField(max_length=64, null=True, blank=True)
    caption = models.CharField(max_length=256, null=True, blank=True)
    plan = models.CharField(max_length=64, null=True, blank=True)
    planCaption = models.CharField(max_length=256, null=True, blank=True)
    see_also = models.ManyToManyField('places.Place',   blank=True)
    def __str__(self):
        return '{t}, {c}'.format (t=self.town, c=self.county)
    class Meta:
        ordering = ['town']

