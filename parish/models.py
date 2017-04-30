from django.db import models

# Create your models here.

class Burial(models.Model):
    date  = models.CharField(max_length=20, null=True, blank=True)
    sort_date  = models.CharField(max_length=15, null=True, blank=True) 
    names = models.CharField(max_length=50, default='Unknown')
    surname = models.CharField(max_length=20, default='Unknown')
    age  = models.CharField(max_length=10, null=True, blank=True)
    source  = models.CharField(max_length=50, null=True, blank=True)
    notes  = models.CharField(max_length=100, null=True, blank=True)
    notebook_ref  = models.CharField(max_length=20, null=True, blank=True)
    orig_ref  = models.CharField(max_length=20, null=True, blank=True)
    place = models.ForeignKey('places.Place', null=True, blank=True)
    person = models.ForeignKey('people.Person', null=True, blank=True)
    def __str__(self):
        return '{n} {s} ({d})'.format(n=self.names, s=self.surname, d=self.date)
    def __event__(self):
        return 'Burial of {n} {s}'.format(n=self.names, s=self.surname)
    event = property(__event__)
    def __ref__(self):
        return 'Burials Index'
    ref=property(__ref__)
    def __path__(self):
        return '/parish/burials/index.html#{id}'.format(id=self.id)
    path=property(__path__)
    def __link_text__(self):
        return 'Burials index'.format(id=self.id)
    link_text=property(__link_text__)
    @property
    def xref(self):
        return 'Burials index'
    class Meta:
        ordering = ['sort_date']

class Marriage(models.Model):
    date = models.CharField(max_length=15, null=True, blank=True)
    sort_date = models.CharField(max_length=15, null=True, blank=True)
    names = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=30, null=True, blank=True)
    spouse = models.CharField(max_length=64, null=True, blank=True)
    age= models.CharField(max_length=5, null=True, blank=True)
    notebook_ref= models.CharField(max_length=10, null=True, blank=True)
    source= models.CharField(max_length=32, null=True, blank=True)
    witnesses= models.CharField(max_length=50, null=True, blank=True)
    notes= models.CharField(max_length=128, null=True, blank=True)
    place = models.ForeignKey('places.Place', null=True, blank=True)
    person = models.ForeignKey('people.Person', null=True, blank=True)
    def __str__(self):
        return '{n} {s} and {sp} ({d})'.format(n=self.names, s=self.surname, sp=self.spouse, d=self.date)
    def __event__(self):
        return 'Marriage of {n} {s} and {sp}'.format(n=self.names, s=self.surname, sp=self.spouse)
    event = property(__event__)
    def __ref__(self):
        return 'Marriage Index'
    ref=property(__ref__)
    def __path__(self):
        return '/parish/marriages/index.html#{id}'.format(id=self.id)
    path=property(__path__)
    def __link_text__(self):
        return 'Marriage index'.format(id=self.id)
    link_text=property(__link_text__)
    @property
    def xref(self):
        return 'Marriage index'
    class Meta:
        ordering=['sort_date']

class Baptism(models.Model):
    date = models.CharField(max_length=20,  null=True, blank=True)
    sort_date = models.CharField(max_length=15, null=True, blank=True)
    names= models.CharField(max_length=30, default="Unknown")
    surname= models.CharField(max_length=20, default="Unknown")
    parents= models.CharField(max_length=100, null=True, blank=True)
    place=models.ForeignKey('places.place', null=True, blank=True, related_name='bb1')
    person = models.ForeignKey('people.person', null=True, blank=True,  related_name='bb2')
    source = models.CharField(max_length=20, null=True, blank=True)
    notebook_code = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return '{n} {s}: {d}'.format(n=self.names, s=self.surname, d=self.date, )
    def __event__(self):
        return 'Baptism of {n} {s}'.format(n=self.names, s=self.surname)
    event = property(__event__)
    def __ref__(self):
        return 'Baptism Index'
    ref=property(__ref__)
    def __path__(self):
        return '/parish/baptisms/index.html#{id}'.format(id=self.id)
    path=property(__path__)
    def __link_text__(self):
        return 'Baptisms index'.format(id=self.id)
    link_text=property(__link_text__)
    @property
    def xref(self):
        return 'Baptism index'
    class Meta:
        ordering = ['sort_date']
