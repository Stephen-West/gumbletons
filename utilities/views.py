from django.shortcuts import render
import re

# Create your views here.

from snippets.models import Snippet
from people.models import Person
from parish.models import Baptism
from skeleton.models import Compendium
from civilreg.models import GRObirth, GROdeath, GROmarriage, BirthCertificate, Death_certificate, MarriageCertificate
from streetsurveys.models import Household, Census, household1939, individual
from string import ascii_uppercase

def admin_check(request):
    snippet_query = Snippet.objects.filter(private=True)
    baptisms = Baptism.objects.all()
    id_list =[]
    for record in baptisms:
        if record.person_id:
            id_list.append(record.person.PID) 
    people_ids = [x for x in id_list if id_list.count(x) != 1]
    people=[]
    for x in people_ids:
        person = Person.objects.get(PID=x)
        people.append(person)
    return render(request, 'utilities/securityadmin.html', {'snippet_query' : snippet_query, 'multiple_baptisms' : people })

def pid_check(request):
    spare_ids={}
    for x in ascii_uppercase:
        people_query = Person.objects.filter(PID__startswith=x).order_by('PID')
        last_id=0
        next_id=0
        for person in people_query:
            id =person.PID[1:5]
            id = int(id)
            if id-last_id>1:
                next_id=last_id+1
                break
            last_id=id
        if not next_id:
            next_id=last_id+2
        spare_ids[x]=next_id
    return render(request, 'utilities/pid_check.html', {'id_list' :spare_ids})
    

def civil_index(url):
    comp = Compendium.objects.get(record_key=url)
    if comp.category == 'births':
        item_list = GRObirth.objects.filter(compendium =comp.id).order_by('sort_date')
    elif comp.category == 'deaths':
        item_list = GROdeath.objects.filter(compendium =comp.id).order_by('sort_date') 
    else:
        item_list = GROmarriage.objects.filter(compendium =comp.id).order_by('sort_date')
    return item_list 

def get_certificates(kind):
    comp = Compendium.objects.get(record_key=kind)
    if kind== 'bcert':
        cert_details = BirthCertificate.objects.all().order_by('id')
    elif kind== 'dcert':
        cert_details = Death_certificate.objects.all().order_by('id')
    else:
        cert_details = MarriageCertificate.objects.all().order_by('id')
    return cert_details

def index_book(request):
    index_list=[]
    certificate_list=[]
    keys = ['ukbirths','ukmarriages','ukdeaths','irelandbirths','irelandmarriages','irelanddeaths',
        'australiabirths', 'australiamarriages', 'australiadeaths','usss_deaths']
    certificates = ['bcert', 'dcert','mcert']
    for item in keys:
        record = {}
        record['index'] = civil_index(item)
        record['key'] = item
        record['compendium'] = Compendium.objects.get(record_key=item)
        index_list.append(record)
    for item in certificates:
        record = {}
        record['detail'] = get_certificates(item)
        record['key'] = item
        record['compendium'] = Compendium.objects.get(record_key=item)
        index_list.append(record)
    return render(request, 'utilities/indexbook.html', {'index_list' : index_list})

def record_book(request):
    indexes=['school', 'universities','apprentices','armed_forces','directories','misc_employment','ppr',
    'wills','ipm','genealogies','news','emigration','tree','papers','other','property','courts',
    'statepapers', 'taxation','poorlaw','pollbooks','ratebooks','residences']
    index_list=[]
    for index in indexes:
        comp= Compendium.objects.get(record_key = index)
        snippet_list = Snippet.objects.filter(group = index).order_by('id')
        for s in snippet_list:
            s.content = re.sub(r'\{\{(.+?)\|person\|.+?\}\}', r'\1', s.content)
            s.content = re.sub(r'<\s*a\s+href.*?>(.*?)<.*?>', r'\1', s.content)
        item = {}
        item['compendium'] = comp
        item['snippet_list'] = snippet_list
        item['title'] = comp.name
        item['rubric'] = comp.rubric
        index_list.append(item)
    context = {'index_list': index_list}
    return render(request, 'utilities/book_template.html', context)

class CensusHousehold:
    id = ""
    title =""
    source_ref=""
    occupants =None
    def __init__(self,id,title,source_ref):
        self.title = title
        self.id = id
        self.source_ref=source_ref
        self.occupants=None
    def add_occupants(self, people):
        self.occupants=(people)
        
class R1939house:
    district=""
    county=""
    surname=""
    unnamed_open= 0
    unnamed_closed=0
    notes=""
    occupants=[]
    id=0
    def __init__(self,id,district,county,surname,unnamed_open,unnamed_closed,notes):
        self.district=district
        self.county=county
        self.surname=surname
        self.unnamed_open=unnamed_open
        self.unnamed_closed=unnamed_closed
        self.notes=notes
        self.id=id
        self.occupants=[]
    def add_occupant(self, person):
        self.occupants.append(person)


        
def get_census(yr):
    #collection_record = Collection.objects.get(year = yr)
    compendium_record = Compendium.objects.get(record_key=yr)
    households = Household.objects.filter(compendium_id= compendium_record.id)
    h_list = []
    for h in households:
        new_household = CensusHousehold(h.id, h.title, h.source_ref)
        occupants = Census.objects.filter(house_id=h.id)
        new_household.add_occupants(occupants)
        h_list.append(new_household)
    return h_list

def census_book(request):
    censuses = [1841, 1851, 1861, 1871, 1881, 1891, 1901, 1911]
    census_list = []
    for census in censuses:
        census_year={}
        census_year['list'] = get_census(census)
        census_list.append(census_year)
        census_year['compendium'] = Compendium.objects.get(record_key=census)
    household_list = household1939.objects.all()
    households=[]
    for house in household_list:
        this_house = R1939house(house.id, house.district, house.county, house.surname, house.unnamed_open,
            house.unnamed_closed, house.notes)
        people_list =individual.objects.filter(household=this_house.id)
        for person in people_list:
            pid=''
            if person.person_id:
                    pid=person.person.PID
            person_record = {'surname' : person.surname, 'names' : person.names , 'birth_year' : person.birth_year ,
                'pid' : pid, 'id' : person.id}
            this_house.add_occupant(person_record)
        households.append(this_house)
    context = {'census_list' : census_list, 'households' : households}
    return render(request, 'utilities/census_template.html', context)

