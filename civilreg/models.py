from django.db import models
from django.db.models import Q

# Create your models here.

class GRObirth(models.Model):
    names= models.CharField(max_length=30, default="Unknown")
    surname= models.CharField(max_length=20, default="Unknown")
    year = models.CharField(max_length=6,  null=True, blank=True)
    quarter = models.CharField(max_length=8,  null=True, blank=True)
    sort_date = models.CharField(max_length=15, null=True, blank=True)
    place = models.ForeignKey('places.Place', null=True, blank=True)
    person = models.ForeignKey('people.Person', null=True, blank=True)
    #mother = models.CharField(max_length=32, null=True, blank=True)
    mother_name = models.CharField(max_length=32, null=True, blank=True)
    #father = models.CharField(max_length=32, null=True, blank=True)
    father_name = models.CharField(max_length=32, null=True, blank=True)
    source = models.CharField(max_length=32, null=True, blank=True)
    reference = models.CharField(max_length=15, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    compendium = models.ForeignKey('skeleton.Compendium', null=True, blank=True)    
    country = models.ForeignKey('places.Country')
    def __str__(self):
        return '{n} {s} ({y})'.format(n=self.names, s=self.surname, y=self.year)    
    class Meta:
        ordering = ['year','sort_date']
    @property
    def event(self):
        return 'Birth registration of {n} {s}'.format(n=self.names, s=self.surname)
    @property
    def date(self):
        return '{y} {q}'.format(y=self.year, q=self.quarter)
    @property
    def link_text(self):
        return 'Civil registration birth registers'
    @property
    def xref(self):
        return self.compendium.name
    @property
    def path(self):
        return '/civilreg/{comp}#{id}'.format(comp = self.compendium.url, id=self.id)

class BcertManager(models.Manager):
    def get_events(self, id):
        """Collate various events and return them as a list of dicts.

        Finds events where the person whose id is 'id' either the person born, the mother
        or the father."""
        event_list=[]
        querylist = self.filter(person=id)
        for entry in querylist:
            event_record = {'sort_date' : entry.sort_date, 'date' : entry.date,
                'event': entry.event, 'place' : entry.place, 'link_text' : 'Birth certificate',
                'event_id' : entry.id, 'path' : '/civilreg/bcert/{id}.html'.format(id=entry.id),
                'xref' : 'Birth certificate'}
            event_list.append(event_record)
        querylist = self.filter(father=id)
        for entry in querylist:
            event_record = {'sort_date' : entry.sort_date, 'date' : entry.date,
                'event': entry.father_event, 'place' : entry.place, 'link_text' : 'Birth certificate',
                'event_id' : entry.id, 'path' : '/civilreg/bcert/{id}.html'.format(id=entry.id),
                'xref' : 'Birth certificate'}
            event_list.append(event_record)
        querylist = self.filter(mother=id)
        for entry in querylist:
            event_record = {'sort_date' : entry.sort_date, 'date' : entry.date,
                'event': entry.mother_event, 'place' : entry.place, 'link_text' : 'Birth certificate',
                'event_id' : entry.id, 'path' : '/civilreg/bcert/{id}.html'.format(id=entry.id),
                'xref' : 'Birth certificate'}
            event_list.append(event_record)

        return event_list

        
class BirthCertificate(models.Model):
    date = models.CharField(max_length=15, null=True, blank=True, help_text='date_registered')
    sort_date = models.CharField(max_length=15, null=True, blank=True)
    born_date = models.CharField(max_length=15, null=True, blank=True, help_text = 'when_born')    
    names= models.CharField(max_length=30, default="Unknown")
    surname= models.CharField(max_length=20, default="Unknown")
    person = models.ForeignKey('people.Person', null=True, blank=True)
    father_name  = models.CharField(max_length=32, null=True, blank=True, help_text = 'father')
    father = models.ForeignKey('people.Person', related_name='f_child', null=True, blank=True)
    father_occupation = models.CharField(max_length=20, null=True, blank=True, help_text='fathers_occ')
    mother_name  = models.CharField(max_length=100, null=True, blank=True, help_text = 'mother')
    mother = models.ForeignKey('people.Person', related_name='m_child', null=True, blank=True)
    place = models.ForeignKey('places.Place', null=True, blank=True)
    subdistrict_name = models.CharField(max_length=50, null=True, blank=True, help_text='subdistrict')
    address_name  = models.CharField(max_length=50, null=True, blank=True, help_text='where_born')
    sex  = models.CharField(max_length=5, null=True, blank=True)
    informant_name  = models.CharField(max_length=100, null=True, blank=True, help_text = 'informant') 
    index_entry = models.ForeignKey('GRObirth', null=True, blank=True, related_name='certificate')
    notes = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return '{n} {s} ({d})'.format(n=self.names, s=self.surname, d=self.date)    
    class Meta:
        ordering = ['sort_date']
    def __event__(self):
        return 'Birth certificate of {n} {s}'.format(n=self.names, s=self.surname)
    event = property(__event__)
    def __mother_event__(self):
        return 'Named as mother in birth certificate of {n} {s}'.format(n=self.names, s=self.surname)
    mother_event = property(__mother_event__)
    def __father_event__(self):
        return 'Named as father in birth certificate of {n} {s}'.format(n=self.names, s=self.surname)
    father_event = property(__father_event__)
    objects = BcertManager()

###################################################################################
#                         GRO Deaths
###################################################################################

class GROdeath(models.Model):
    names= models.CharField(max_length=30, default="Unknown")
    surname= models.CharField(max_length=20, default="Unknown")
    year = models.CharField(max_length=6,  null=True, blank=True)
    quarter = models.CharField(max_length=8,  null=True, blank=True)
    sort_date = models.CharField(max_length=15, null=True, blank=True)
    place = models.ForeignKey('places.Place', null=True, blank=True)
    person = models.ForeignKey('people.Person', null=True, blank=True)
    mother_name = models.CharField(max_length=32, null=True, blank=True)
    father_name = models.CharField(max_length=32, null=True, blank=True)
    age = models.CharField(max_length=10, null=True, blank=True)
    birth_date  = models.CharField(max_length=15, null=True, blank=True)
    source = models.CharField(max_length=32, null=True, blank=True)
    reference = models.CharField(max_length=15, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    compendium = models.ForeignKey('skeleton.Compendium', null=True, blank=True)    
    country = models.ForeignKey('places.Country')
    def __str__(self):
        return '{n} {s} ({y})'.format(n=self.names, s=self.surname, y=self.year)    
    class Meta:
        ordering = ['year','sort_date']
    def __event__(self):
        return 'Death registration of {n} {s}'.format(n=self.names, s=self.surname)
    event = property(__event__)
    def __date__(self):
        return '{y} {q}'.format(y=self.year, q=self.quarter)
    date = property(__date__)
    def __link_text__(self):
        return 'Civil registration death registers'
    link_text = property(__link_text__)    
    @property
    def xref(self):
        return self.compendium.name
    def __path__(self):
        return '/civilreg/{comp}#{id}'.format(comp = self.compendium.url, id=self.id)
    path = property(__path__)    

class DcertManager(models.Manager):
    def get_events(self, id):
        """Collate various events and return them as a list of dicts.

       ."""
        event_list=[]
        querylist = self.filter(person=id)
        for entry in querylist:
            event_record = {'sort_date' : entry.date, 'date' : entry.date,
                'event': entry.death_event, 'place' : entry.place, 'link_text' : 'Death certificate',
                'event_id' : entry.id, 'path' : '/civilreg/dcert/{id}.html'.format(id=entry.id),
                'xref' : 'Death certificate'}
            event_list.append(event_record)
        querylist = self.filter(other_people=id)
        for entry in querylist:
            event_record = {'sort_date' : entry.date, 'date' : entry.date,
                'event': entry.other_event, 'place' : entry.place, 'link_text' : 'Death certificate',
                'event_id' : entry.id, 'path' : '/civilreg/dcert/{id}.html'.format(id=entry.id),
                'xref' : 'Death certificate'}
            event_list.append(event_record)
        return event_list

class Death_certificate(models.Model):
    district = models.CharField(max_length=32, null=True, blank=True)
    subdistrict = models.CharField(max_length=32, null=True, blank=True)
    date = models.CharField(max_length=20, null=True, blank=True, help_text="When died")
    where_died = models.CharField(max_length=64, null=True, blank=True)
    place = models.ForeignKey('places.Place', null=True, blank=True)
    names = models.CharField(max_length=32, null=True, blank=True)
    surname = models.CharField(max_length=32, null=True, blank=True)
    person = models.ForeignKey('people.Person', null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    age  = models.CharField(max_length=8, null=True, blank=True)
    occupation = models.CharField(max_length=64, null=True, blank=True)
    cause = models.CharField(max_length=256, null=True, blank=True)
    informant = models.CharField(max_length=256, null=True, blank=True)
    date_registered = models.CharField(max_length=15, null=True, blank=True)
    registrar = models.CharField(max_length=32, null=True, blank=True)
    notes = models.CharField(max_length=64, null=True, blank=True)
    index_entry = models.ForeignKey('GROdeath', null=True, blank=True, related_name='certificate')
    other_people=  models.ManyToManyField('people.Person',   blank=True, related_name='dcert')
    objects=DcertManager()
    @property
    def sort_date(self):
        return self.date
    @property
    def death_event(self):
        return "Death certificate of {n} {s}".format(n=self.names, s=self.surname)
    @property
    def other_event(self):
        return "Named in death certificate of {n} {s}".format(n=self.names, s=self.surname)
    def __str__(self):
        return '{n} {s}'.format(n=self.names, s=self.surname)    
    class Meta:
        ordering = ['date_registered']
###################################################################################
#                         GRO Marriages
###################################################################################

class GROmarriage(models.Model):
    names= models.CharField(max_length=30, default="Unknown")
    surname= models.CharField(max_length=20, default="Unknown")
    year = models.CharField(max_length=6,  null=True, blank=True)
    quarter = models.CharField(max_length=8,  null=True, blank=True)
    sort_date = models.CharField(max_length=15, null=True, blank=True)
    place = models.ForeignKey('places.Place', null=True, blank=True)
    person = models.ForeignKey('people.Person', null=True, blank=True)
    spouse_name = models.CharField(max_length=32, null=True, blank=True)
    spouse = models.ForeignKey('people.Person', null=True, blank=True, related_name='spouse')
    source = models.CharField(max_length=15, null=True, blank=True)
    reference = models.CharField(max_length=15, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    compendium = models.ForeignKey('skeleton.Compendium', null=True, blank=True)    
    country = models.ForeignKey('places.Country')
    def __str__(self):
        return '{n} {s} ({y})'.format(n=self.names, s=self.surname, y=self.year)    
    class Meta:
        ordering = ['year','sort_date']
    def __event__(self):
        return 'Marriage registration of {n} {s}'.format(n=self.names, s=self.surname)
    event = property(__event__)
    def __date__(self):
        return '{y} {q}'.format(y=self.year, q=self.quarter)
    date = property(__date__)
    def __link_text__(self):
        return 'Civil marriage registers'
    link_text = property(__link_text__)    
    @property
    def xref(self):
        return self.compendium.name
    def __path__(self):
        return '/civilreg/{url}#{id}'.format(url=self.compendium.url,id=self.id)
    path = property(__path__)    

class McertManager(models.Manager):
    def get_events(self, id):
        """Collate various events and return them as a list of dicts.

        Finds events where the person whose id is 'id' either the person married, 
        the father or a witness."""
        event_list=[]
        querylist = self.filter(Q(man=id) | Q(woman=id))
        for entry in querylist:
            event_record = {'sort_date' : entry.date, 'date' : entry.date,
                'event': entry.man_event, 'place' : entry.place_name, 'link_text' : 'Marriage certificate',
                'event_id' : entry.id, 'path' : '/civilreg/mcert/{id}.html'.format(id = entry.id),
                'xref' : 'Marriage certificate'}
            event_list.append(event_record)
        querylist = self.filter(Q(man_father=id) | Q(woman_father=id))
        for entry in querylist:
            event_record = {'sort_date' : entry.date, 'date' : entry.date,
                'event': entry.father_event, 'place' : entry.place_name, 'link_text' : 'Marriage certificate',
                'event_id' : entry.id, 'path' : '/civilreg/mcert/{id}.html'.format(id = entry.id),
                'xref' : 'Marriage certificate'}
            event_list.append(event_record)
        querylist = self.filter(witnesses=id)
        for entry in querylist:
            event_record = {'sort_date' : entry.date, 'date' : entry.date,
                'event': entry.witness_event, 'place' : entry.place_name, 'link_text' : 'Marriage certificate',
                'event_id' : entry.id, 'path' : '/civilreg/mcert/{id}.html'.format(id = entry.id),
                'xref' : 'Marriage certificate'}
            event_list.append(event_record)
        return event_list

class MarriageCertificate(models.Model):
    date = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=64, null=True, blank=True)
    place_name = models.CharField(max_length=32, null=True, blank=True)
    county = models.ForeignKey('places.County', null=True, blank=True)
    man_name = models.CharField(max_length=64, null=True, blank=True)
    man = models.ForeignKey('people.Person', null=True, blank=True, related_name='husband')
    man_code = models.CharField(max_length=15, null=True, blank=True)
    man_age  = models.CharField(max_length=8, null=True, blank=True)
    man_condition = models.CharField(max_length=20, null=True, blank=True)
    man_occupation = models.CharField(max_length=64, null=True, blank=True)
    man_residence = models.CharField(max_length=128, null=True, blank=True)
    man_father_name = models.CharField(max_length=64, null=True, blank=True)
    man_father = models.ForeignKey('people.Person', null=True, blank=True, related_name='son_marriage')
    man_fathers_occupation = models.CharField(max_length=128, null=True, blank=True)
    man_father_code = models.CharField(max_length=15, null=True, blank=True)
    woman_name = models.CharField(max_length=64, null=True, blank=True)
    woman = models.ForeignKey('people.Person', null=True, blank=True, related_name='wife')
    woman_code = models.CharField(max_length=15, null=True, blank=True)
    woman_age  = models.CharField(max_length=8, null=True, blank=True)
    woman_condition = models.CharField(max_length=20, null=True, blank=True)
    woman_occupation = models.CharField(max_length=64, null=True, blank=True)
    woman_residence = models.CharField(max_length=128, null=True, blank=True)
    woman_father_name = models.CharField(max_length=64, null=True, blank=True)
    woman_father = models.ForeignKey('people.Person', null=True, blank=True, related_name='daughter_marriage')
    woman_fathers_occupation = models.CharField(max_length=64, null=True, blank=True)
    woman_father_code = models.CharField(max_length=15, null=True, blank=True)
    married_at = models.CharField(max_length=128, null=True, blank=True)
    witness_names = models.CharField(max_length=256, null=True, blank=True)
    witnesses =  models.ManyToManyField('people.Person',   blank=True)
    index_entry = models.ForeignKey('GROmarriage', null=True, blank=True, related_name='certificate')
    notes = models.CharField(max_length=256, null=True, blank=True)
    margin_notes = models.CharField(max_length=256, null=True, blank=True)
    def __str__(self):
        return '{m} and {w}'.format(m=self.man_name, w=self.woman_name)    
    def __sort_date__(self):    
        return self.date
    sort_date=property(__sort_date__)
    def __man_event__(self):
        return 'Marriage certificate of {m} and {w}'.format(m=self.man_name, w=self.woman_name)
    man_event = property(__man_event__)
    def __father_event__(self):
        return 'Named as father in marriage certificate of {m} and {w}'.format(m=self.man_name, w=self.woman_name)
    father_event = property(__father_event__)
    def __witness_event__(self):
        return 'Named as a witness in marriage certificate of {m} and {w}'.format(m=self.man_name, w=self.woman_name)
    witness_event = property(__witness_event__)
    objects = McertManager()
    class Meta:
        ordering = ['date']
