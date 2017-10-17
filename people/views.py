from django.shortcuts import render
from django.db.models import Q
from .models import Person, Spouse
from streetsurveys.models import ElectoralRolls, individual,Census
from civilreg.models import GRObirth, BirthCertificate, GROdeath, GROmarriage, MarriageCertificate, Death_certificate
from snippets.models import Snippet
from parish.models import Burial, Baptism, Marriage
from utilities.privacy_filters import sp_filter, sanitize, people_filter
from utilities.urlfilters import preparse, heading_down
from datetime import datetime,date

today = date.today()
century_date = str(date(today.year -100, today.month, today.day))


# Create your views here.
source_list = [ElectoralRolls, GRObirth, GROdeath, GROmarriage, individual, Burial, Baptism, Marriage, Census]
complex_source_list = [BirthCertificate, Snippet, MarriageCertificate, Death_certificate]

def show_person( request, pid):
    person_record = Person.objects.get(PID = pid)
    person_record.biography = preparse(person_record.biography)
    id = person_record.id
#If the father or mother don't have a name, get it from their people records
    if not person_record.father_name:
        person_record.father_name= person_record.father.name if person_record.father_id else ''
    if not person_record.mother_name:
        person_record.mother_name= person_record.mother.name if person_record.mother_id else ''
#If no baptism entry or burial entry, check for foreign keys from baptism or burial
    if not person_record.baptism_date:
        try:
            if Baptism.objects.filter(person_id=id).exists():
                bapt = Baptism.objects.get(person_id=id)
                person_record.baptism_date = bapt.date
                person_record.baptism_place = bapt.place 
        except:
            print ("Error in getting baptism for person {p}".format(p=pid))               
    if not person_record.burial_date:
        try:
            if Burial.objects.filter(person_id=id).exists():
                burial = Burial.objects.get(person_id=id)
                person_record.burial_date = burial.date
                person_record.burial_place = burial.place    
        except:
            print ("Error in getting burial for person {p}".format(p=pid))     
    if not person_record.birth_date:
        try:
            if GRObirth.objects.filter(person_id=id).exists():
                birth = GRObirth.objects.get(person_id=id)
                person_record.birth_date = birth.year
                person_record.birth_place = birth.place    
        except:
            print ("Error in getting birth for person {p}".format(p=pid))      
    if not person_record.death_date:
        try:
            if GROdeath.objects.filter(person_id=id).exists():
                death = GROdeath.objects.get(person_id=id)
                person_record.death_date = death.year
                person_record.death_place = death.place    
        except:
            print ("Error in getting birth for person {p}".format(p=pid))         
#Assemble information about spouses
    spouse_list=[]
    if person_record.sex.upper() == 'M':
        spouses = sp_filter(Spouse.objects.filter(man = person_record.id))
        for i, s in enumerate(spouses):
            name =  s.woman.name
            death_date = s.woman.death_date
            death_place = s.woman.death_place
            children = people_filter(
                Person.objects.filter(father=s.man).filter(mother=s.woman).order_by('birth_date'))
            child_list = []
            for j, c in enumerate(children):
                child = {'pid' : c.PID, 'ordinal' : j+1, 'birth_date' : c.birth_date}
                child['name'] = c.name
                child_list.append(child)
                
            spouse_list.append({'ordinal' : i+1, 'name' : name, 'pid' : s.woman.PID, 
                'date' : s.date, 'place' : s.place, 'death_date' : death_date, 'death_place' : death_place,
				'divorced' : s.divorced, 'divorce_date': s.divorce_date,
                'child_list' : child_list})

    else:
        spouses = sp_filter(Spouse.objects.filter(woman = person_record.id))
        for i, s in enumerate(spouses):
            name =  s.man.name
            death_date = s.man.death_date
            death_place = s.man.death_place
            children = people_filter(Person.objects.filter(father=s.man).filter(mother=s.woman).order_by('birth_date'))
            child_list = []
            for j, c in enumerate(children):
                child = {'pid' : c.PID, 'ordinal' : j+1, 'birth_date' : c.birth_date}
                child['name'] = c.name
                child_list.append(child)
            spouse_list.append({'ordinal' : i+1, 'name' : name, 'pid' : s.man.PID, 
                'date' : s.date, 'place' : s.place, 'death_date' : death_date, 'death_place' : death_place,
				'divorced' : s.divorced, 'divorce_date': s.divorce_date,
                'child_list' : child_list})

        
    event_list = []
    for source in source_list:
        eventquery = source.objects.filter(person =person_record.id)
        for event in eventquery:
            try:
                place=event.place
            except:
                place=""
            event_record = {'sort_date' : event.sort_date, 'date' : event.date,
                'event': event.event, 'place' : place, 'link_text' : event.link_text,
                'event_id' : event.id, 'path' : event.path}
            event_list.append(event_record)
    for source in complex_source_list:
        results = source.objects.get_events(person_record.id)
        if results:
            event_list.extend(results)
    event_list =sorted(event_list, key=lambda tup: tup['sort_date'])
    #print ("Event list: ",event_list)
    recent = False
    if person_record.birth_date:
        if person_record.birth_date > "1900-01-01":
            recent=True
    context = {'person_record': person_record, 'spouse_list' : spouse_list, 
            'event_list' : event_list, 'recent' : recent}
    return render(request, 'people/person.html', context)

def people_index(request):
    p_record = people_filter(Person.objects.all())
    return render(request, 'people/people_index.html', {'p_record' : p_record, 'title' : "Index of all people pages", })

def private_people(request):
    #today=datetime.now().strftime('%Y-%m-%d')
    p_record = people_filter(Person.objects.exclude(birth_date__isnull=True).filter(birth_date__lt = century_date).filter(private=True))
    return render(request, 'people/people_index.html', {'p_record' : p_record, 'title' : "Private people over 100", })

def public_people(request):
    p_record = people_filter(Person.objects.filter(birth_date__gt = century_date).filter(private=False))
    return render(request, 'people/people_index.html', {'p_record' : p_record, 'title' : "Public people under 100", })

def nongumbleton_index(request):
    q1=Q(surname__istartswith='Gum')
    q2= Q(surname__istartswith='Gam')
    q3= Q(surname__istartswith='Gom')
    q4=Q(surname__istartswith='Gimble')
    q5=Q(surname__istartswith='Grum')
    q6=Q(surname__istartswith='Cumblet')
    q7=Q(surname__istartswith='Comblet')
    q8=Q(surname='WEST')
    q9=Q(surname__icontains='Gumblet')

    p_record = people_filter(
        Person.objects.exclude(q1).exclude(q2).exclude(q3).exclude(q4).exclude(q5).exclude(q6).exclude(q7).exclude(q8).exclude(q9))
    return render(request, 'people/people_index.html', {'p_record' : p_record, 'title' : "Index of non-Gumbleton people" })

def gumbleton_index(request):
    q1=Q(surname__istartswith='Gum')
    q2= Q(surname__istartswith='Gam')
    q3= Q(surname__istartswith='Gom')
    q4=Q(surname__istartswith='Gimble')
    q5=Q(surname__istartswith='Grum')
    q6=Q(surname__istartswith='Cumblet')
    q7=Q(surname__istartswith='Comblet')
    q8=Q(surname='WEST')
    q9=Q(surname__icontains='Gumblet')
    g_record = people_filter(
        Person.objects.exclude(q1).exclude(q2).exclude(q3).exclude(q4).exclude(q5).exclude(q6).exclude(q7).exclude(q8).exclude(q9))
    a_record= people_filter(Person.objects.all())
    p_record = a_record.exclude(pk__in = g_record)
    return render(request, 'people/people_index.html', {'p_record' : p_record, 'title' : "Index of people pages for Gumbletons and variants" })
    

############################## Experimental stuff #####################################

def get_events(person_id):
    event_list = []
    for source in source_list:
        #print (person_record.id)
        eventquery = source.objects.filter(person =person_id)
        for event in eventquery:
            try:
                place=event.place
            except:
                place=""
            event_record = {'sort_date' : event.sort_date, 'date' : event.date,
                'event': event.event, 'place' : place, 'link_text' : event.link_text,
                'event_id' : event.id, 'path' : event.path}
            try:
                event_record['xref'] = event.xref
            except:
                pass
            #print ("Event record: ",event_record)
            event_list.append(event_record)
    for source in complex_source_list:
        results = source.objects.get_events(person_id)
        if results:
            event_list.extend(results)
    event_list =sorted(event_list, key=lambda tup: tup['sort_date'])
    return event_list

def get_spouses(person_record):
    print (person_record)
    spouse_list=[]
    if person_record.sex.upper() == 'M':
        spouses = sp_filter(Spouse.objects.filter(man = person_record.id))
        for i, s in enumerate(spouses):
            name =  s.woman.name
            death_date = s.woman.death_date
            death_place = s.woman.death_place
            children = people_filter(
                Person.objects.filter(father=s.man).filter(mother=s.woman).order_by('birth_date'))
            child_list = []
            for j, c in enumerate(children):
                child = {'pid' : c.PID, 'ordinal' : j+1, 'birth_date' : c.birth_date}
                child['name'] = c.name
                child_list.append(child)
                
            spouse_list.append({'ordinal' : i+1, 'name' : name, 'pid' : s.woman.PID, 
                'date' : s.date, 'place' : s.place, 'death_date' : death_date, 'death_place' : death_place,
                'child_list' : child_list})
    else:
        spouses = sp_filter(Spouse.objects.filter(woman = person_record.id))
        for i, s in enumerate(spouses):
            name =  s.man.name
            death_date = s.man.death_date
            death_place = s.man.death_place
            children = people_filter(Person.objects.filter(father=s.man).filter(mother=s.woman))
            child_list = []
            for j, c in enumerate(children):
                child = {'pid' : c.PID, 'ordinal' : j+1, 'birth_date' : c.birth_date}
                child['name'] = c.name
                child_list.append(child)
            spouse_list.append({'ordinal' : i+1, 'name' : name, 'pid' : s.man.PID, 
                'date' : s.date, 'place' : s.place, 'death_date' : death_date, 'death_place' : death_place,
                'child_list' : child_list})
    return spouse_list


