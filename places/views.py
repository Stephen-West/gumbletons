from django.shortcuts import render
from .models import Place
from streetsurveys.models import ElectoralRolls, individual,Census
from civilreg.models import GRObirth, BirthCertificate, GROdeath, GROmarriage, MarriageCertificate, Death_certificate
from snippets.models import Snippet
from parish.models import Burial, Baptism, Marriage
from utilities.privacy_filters import sp_filter, sanitize, people_filter
from datetime import datetime,date

# Create your views here.

source_list = [GRObirth, GROdeath, GROmarriage,  Burial, Baptism, Marriage]

def show_place(request,  id):
    place = Place.objects.get(id = id)
    event_list = []
    for source in source_list:
        eventquery = source.objects.filter(place = id)
        for event in eventquery:
            try:
                person=event.person
            except:
                person=""
            event_record = {'sort_date' : event.sort_date, 'date' : event.date,
                'event': event.event, 'person' : person, 'link_text' : event.link_text,
                'event_id' : event.id, 'path' : event.path}
            event_list.append(event_record)
    event_list =sorted(event_list, key=lambda tup: tup['sort_date'])
    context = {'place' : place, 'event_list' : event_list}
    return render(request, 'places/place.html', context)
