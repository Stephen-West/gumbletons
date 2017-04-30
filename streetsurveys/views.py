from django.shortcuts import render

from .models import ElectoralRolls, household1939, individual,  Household, Census
from skeleton.models import Compendium

 
# Create your views here.
def rolls_index(request):
    roll_list = ElectoralRolls.objects.all()
    years_list = []
    for record in roll_list:
        years_list.append(record.year)
    years=set(years_list)
    years=sorted(years)
    context = {'years': years}
    return render(request, 'streetsurveys/electoral.html', context)

class houshold_object:
    address_name =""
    place_name=""
    occupants =[]
    id = ""
    def __init__(self,address, place, occ_list):
        self.address_name = address
        self.occupants=occ_list
        self.place_name=place
    def add_occupant(self, person):
        self.occupants.append(person)

def prepare_datastructures(query):
    if query:
        address_list = []
        for record in query:
            #print (record)
            address_list.append(record.address_name)
        address_list = sorted(set(address_list))
        #print (address_list)
        households=[]
        for a in address_list:
            occ_list = query.filter(address_name=a)
            first_occ=occ_list.all()[:1].get()
            ho = houshold_object(a, first_occ.place_name, occ_list)    
            households.append(ho)
            #print (a,ho.address_name)
        return households
    else:
        return 0

def rolls_year(request,yr):
    roll_list = ElectoralRolls.objects.filter(year = yr)
    #Need one record from list to check if this is a year with spring and autumn records
    first_roll = roll_list.all()[:1].get()
    seasons=1
    #yr=0
    if first_roll.season:
        #We have a spring/autumn year
        seasons=2
        households_1 = prepare_datastructures(roll_list.filter(season= "Spring"))
        households_2 = prepare_datastructures(roll_list.filter(season='Autumn'))
    else:
        #Normal year
        households_1 = prepare_datastructures(roll_list)
        households_2=0
    context = {'households_1' : households_1, 
        'households_2' : households_2, 'seasons' : seasons, 'year' : yr}
    return render( request, 'streetsurveys/electoralyear.html', context)

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

def R1939index(request):
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
    context = {'households' : households}
    return render( request, 'streetsurveys/r1939.html', context)

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
        
        
def census(request, yr):
    #collection_record = Collection.objects.get(year = yr)
    compendium_record = Compendium.objects.get(record_key=yr)
    households = Household.objects.filter(compendium_id= compendium_record.id)
    h_list = []
    for h in households:
        new_household = CensusHousehold(h.id, h.title, h.source_ref)
        occupants = Census.objects.filter(house_id=h.id)
        new_household.add_occupants(occupants)
        h_list.append(new_household)
    template="streetsurveys/{t}".format(t=compendium_record.template)
    return render(request, template, {'c_record' : compendium_record, 'households': h_list, })

