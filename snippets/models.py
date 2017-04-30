from django.db import models
from people.models import Person

# Create your models here.

class SnippetManager(models.Manager):
    def get_events(self, id):
        """Collate various events and return them as a list of dicts.

        Finds events where the person whose id is 'id' either the person born, the mother
        or the father."""
        event_list=[]
        person = Person.objects.get(id=id)
        name = "{n} {s}".format(n=person.names, s=person.surname)
        querylist = self.filter(person=id)
        for entry in querylist:
            event_record = {'sort_date' : entry.sort_date, 'date' : entry.date,
                'event': entry.title, 'place' : entry.place, 'link_text' : 'View details',
                'event_id' : entry.id, 'path' : '{pre}{grp}/{id}.html'.format(pre=entry.compendium.prefix, grp=entry.group, id=entry.id),
                'xref' : '{comp}: item  no. {n}'.format(comp=entry.compendium.name, n=entry.id)}
            event_list.append(event_record)
        querylist = self.filter(other_names=id)
        for entry in querylist:
            event_record = {'sort_date' : entry.sort_date, 'date' : entry.date,
                'event': '{p} referenced in {t}'.format(p=name,t=entry.title), 
                'place' : entry.place, 'link_text' : 'View details',
                'event_id' : entry.id, 'path' : '{pre}{grp}/{id}.html'.format(pre=entry.compendium.prefix, grp=entry.group, id=entry.id),
                'xref' : '{comp}: item  no. {n}'.format(comp=entry.compendium.name, n=entry.id)}
            event_list.append(event_record)
        return event_list

class Snippet(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    date = models.CharField(max_length=16, null=True, blank=True)
    sort_date  = models.CharField(max_length=16, null=True, blank=True)
    person = models.ForeignKey('people.Person', null=True, blank=True, related_name="related")
    name = models.CharField(max_length=64, null=True, blank=True)
    person_code = models.CharField(max_length=16, null=True, blank=True)
    place = models.CharField(max_length=64, null=True, blank=True)
    content = models.TextField(blank=True)   
    other_names = models.ManyToManyField('people.Person',   blank=True)
    source = models.CharField(max_length=128, null=True, blank=True)
    reference = models.CharField(max_length=32, null=True, blank=True) 
    transcriber =models.CharField(max_length=128, null=True, blank=True)
    picture = models.CharField(max_length=64, null=True, blank=True)
    caption = models.CharField(max_length=256, null=True, blank=True)    
    group = models.CharField(max_length=32, null=True, blank=True)
    compendium = models.ForeignKey('skeleton.Compendium')
    private = models.BooleanField(default=False)
    notes = models.TextField(blank=True)  
    class Meta:
        ordering = ['sort_date']
    def __str__(self):
        return self.title    
    @property
    def event(self):
        return self.title
    @property
    def link_text(self):
        return 'View details'
    @property
    def path(self):
        return '{pre}{grp}/{id}.html'.format(pre=entry.compendium.prefix, grp=entry.group, id=entry.id)
    objects = SnippetManager()        

