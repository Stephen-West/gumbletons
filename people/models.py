from django.db import models


# Create your models here.

         
class Person(models.Model):
    PID = models.CharField(max_length=10, db_index=True, unique=True)
    names = models.CharField(max_length=50, default='Unknown')
    surname = models.CharField(max_length=32, default='Unknown')
    birth_date = models.CharField(max_length=20, null=True, blank=True)
    birth_place = models.ForeignKey('places.Place', null=True, blank=True, related_name='b1')
    baptism_date = models.CharField(max_length=20, null=True, blank=True)
    baptism_place = models.ForeignKey('places.Place', null=True, blank=True, related_name='b2')
    death_date = models.CharField(max_length=20, null=True, blank=True)    
    death_place = models.ForeignKey('places.Place', null=True, blank=True,
        related_name='b3')
    burial_date = models.CharField(max_length=15, null=True, blank=True)
    burial_place = models.ForeignKey('places.Place', null=True, blank=True, related_name='b4')
    sex = models.CharField(max_length=10, null=True, blank=True)    
    father_name = models.CharField(max_length=40, null=True, blank=True, help_text=
        "Used if Father field left blank")    
    mother_name = models.CharField(max_length=40, null=True, blank=True, help_text=
        "Used if Mother field left blank")
    father = models.ForeignKey('self', related_name='child', null=True, blank=True)
    mother = models.ForeignKey('self', related_name='childA', null=True, blank=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    picture = models.CharField(max_length=20, null=True, blank=True)
    caption = models.CharField(max_length=250, null=True, blank=True)
    listed = models.BooleanField(default=True)
    private =  models.BooleanField(default=False)
    credit = models.CharField(max_length=120, null=True, blank=True, help_text="Credit for biographical information")
    def __str__(self):
        return '{n} {s} ({b} - {d}) [{id}]'.format(
            n=self.names, s=self.surname, b=self.birth_date, 
            d=self.death_date, id=self.PID)
    @property
    def name (self):
        return '{n} {s}'.format(n=self.names, s=self.surname)
    class Meta:
        ordering = ['surname','names','PID']    

class Spouse(models.Model):
    man = models.ForeignKey('Person', related_name='marriage1', null=True, blank=True)
    woman = models.ForeignKey('Person', related_name='marriage2', null=True, blank=True)
    man_code = models.CharField(max_length=10, null=True, blank=True, help_text="For migration use only")
    woman_code = models.CharField(max_length=10, null=True, blank=True, help_text="For migration use only")
    date = models.CharField(max_length=20, null=True, blank=True, help_text="Date of marriage, if known")
    sort_date = models.CharField(max_length=20, null=True, blank=True)
    place = models.ForeignKey('places.Place', null=True, blank=True, related_name='sp')
    place_code = models.CharField(max_length=10, null=True, blank=True)
    notes =  models.CharField(max_length=255, null=True, blank=True)
    divorced = models.BooleanField(default=False)
    divorce_date = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return '{m} : {w} ({d})'.format(m=self.man, w=self.woman, d=self.date, )
    @property
    def private(self):
        if self.woman_id and self.woman.private:
            return True
        if self.man_id and self.man.private:
            return True
        return False
    @property
    def man_name(self):
        if self.man_id:
            return self.man.name
        else:
            return ''
    class Meta:
        ordering = ['sort_date']

