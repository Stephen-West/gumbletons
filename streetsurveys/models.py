from django.db import models

# Create your models here.

class Address(models.Model):
    address = models.CharField(max_length=100)
    def __str__(self):
        return self.address    
    class Meta:
        ordering = ['address']


class ElectoralRolls(models.Model):
    names= models.CharField(max_length=30, default="Unknown")
    surname= models.CharField(max_length=20, default="Unknown")
    person = models.ForeignKey('people.Person', null=True, blank=True)
    year = models.CharField(max_length=6,  null=True, blank=True)
    season = models.CharField(max_length=8,  null=True, blank=True)
    sort_date = models.CharField(max_length=15, null=True, blank=True)
    place = models.ForeignKey('places.Place', null=True, blank=True)
    place_name = models.CharField(max_length=100, null=True, blank=True)
    address=models.ForeignKey('Address', null=True, blank=True)
    address_name = models.CharField(max_length=100, null=True, blank=True)
    local_qual = models.CharField(max_length=60, null=True, blank=True)
    national_qual = models.CharField(max_length=60, null=True, blank=True)
    qual_property = models.CharField(max_length=100, null=True, blank=True)
    juror = models.CharField(max_length=5, null=True, blank=True)
    source = models.CharField(max_length=30, null=True, blank=True)
    reference = models.CharField(max_length=15, null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return '{n} {s} ({y}): {a}'.format(n=self.names, s=self.surname, y=self.year,
            a=self.address)    
    class Meta:
        ordering = ['year','place_name', 'sequence']
    def __event__(self):
        return '{n} {s} living at {a}'.format(n=self.names, s=self.surname, a=self.address)
    event = property(__event__)
    def __date__(self):
        return '{y} {s}'.format(y=self.year, s=self.season)
    date = property(__date__)
    def __link_text__(self):
        return 'Electoral rolls'
    link_text = property(__link_text__)    
    def __path__(self):
        return '/staterecords/electoralrolls/{y}.html#{id}'.format(y=self.year, id=self.id)
    path = property(__path__)    
    @property
    def xref(self):
        return 'Electoral rolls, {yr}'.format(yr=self.year)

class household1939(models.Model):
    district = models.CharField(max_length=100)
    county = models.ForeignKey('places.County', null=True, blank=True)
    surname = models.CharField(max_length=30)
    unnamed_open = models.IntegerField(null=True, blank=True)
    unnamed_closed = models.IntegerField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return '{d} {c} ({n} household)'.format(d=self.district, c=self.county, n=self.surname)    
    class Meta:
        ordering = ['county', 'district']


class individual(models.Model):
    names= models.CharField(max_length=30, null=True, blank=True)
    surname= models.CharField(max_length=20, null=True, blank=True)
    person = models.ForeignKey('people.Person', null=True, blank=True)
    birth_year= models.CharField(max_length=5, null=True, blank=True)
    household = models.ForeignKey('household1939', null=True, blank=True)
    def __str__(self):
        return '{n} {s} ({b})'.format(n=self.names, s=self.surname, b=self.birth_year)    
    class Meta:
        ordering = ['surname', 'names']
    def __place__(self):
        return  self.household.district
    place = property(__place__)
    def __event__(self):
        return '1939 Register: {n} {s} living in {p}'.format(n=self.names, s=self.surname, p=self.place)
    event = property(__event__)
    def __date__(self):
        return '1939-06-01'
    date = property(__date__)
    def __sort_date__(self):
        return ('1939-06-01')
    sort_date = property(__sort_date__)
    def __link_text__(self):
        return '1939 Register'
    link_text = property(__link_text__)    
    def __path__(self):
        return '/census/r1939.html#{person}'.format(person=self.id)
    path = property(__path__)    
    @property
    def xref(self):
        return '1939 index'

#####################Census ###########################################
 
    
class Household(models.Model):
    compendium = models.ForeignKey('skeleton.Compendium', null=True, blank=True)
    title= models.CharField(max_length=100, null=True, blank=True)
    source_ref= models.CharField(max_length=40, null=True, blank=True)
    sequence= models.IntegerField(null=True, blank=True)
    repository_id= models.CharField(max_length=20, null=True, blank=True)
    place_code = models.CharField(max_length=10, null=True, blank=True)
    place = models.ForeignKey('places.Place', null=True, blank=True)
    def __str__(self):
        try:
            return '{t} ({p})'.format(t=self.title, p=self.parent)
        except:
            return self.title
    class Meta:
        ordering = ['sequence']    
        
class Census(models.Model):
    house= models.ForeignKey('Household',null=True, blank=True)
    sort_order= models.IntegerField(null=True, blank=True)
    relation=models.CharField(max_length=15, null=True, blank=True)
    status=models.CharField(max_length=3, null=True, blank=True)
    name=models.CharField(max_length=50, null=True, blank=True)
    born=models.CharField(max_length=50, null=True, blank=True)
    occupation=models.CharField(max_length=50, null=True, blank=True)
    age=models.CharField(max_length=5, null=True, blank=True)
    person= models.ForeignKey('people.Person', null=True, blank=True)
    religion= models.CharField(max_length=63, null=True, blank=True)
    education= models.CharField(max_length=63, null=True, blank=True)
    languages= models.CharField(max_length=63, null=True, blank=True)
    notes=models.CharField(max_length=15, null=True, blank=True)
    @property
    def census_year(self):
        try:
            year=self.house.compendium.record_key.rstrip('i')
        except:
            year='unknown'
            print ("Exception in record {id}, household {h}".format(id= self.id, h=self.house_id))
        return year
    def __str__(self):
        return '{n} ({y}) age {a}'.format(n=self.name, a=self.age, y=self.census_year)
    @property
    def event(self):
        if self.age:
            return '{n} (age {a}) living in {p} in {y} census'.format(
                n=self.name, a=self.age, p=self.house.title, y=self.census_year)        
        else:
            return '{n} living in {p} in {y} census'.format(n=self.name, p=self.house.title, y=self.census_year)
    @property
    def sort_date(self):
        return self.house.compendium.sort_date
    @property
    def date(self):
        return self.sort_date
    @property
    def place(self):
        return self.house.place
    @property
    def link_text(self):
        return '{y} census'.format(y=self.census_year)
    @property
    def path(self):
        return '/census/{y}.html#{id}'.format(y=self.house.compendium.record_key, id=self.id)
    @property
    def xref(self):
        return '{y} Census'.format(y=self.house.compendium.record_key)
    class Meta:
        ordering = ['house__compendium__record_key','sort_order']    
