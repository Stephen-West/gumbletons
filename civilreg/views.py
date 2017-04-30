from django.shortcuts import render

# Create your views here.

from .models import GRObirth, GROdeath, GROmarriage, BirthCertificate, MarriageCertificate, Death_certificate
from skeleton.models import Compendium
from people.models import Person
from utilities.privacy_filters import sanitize


########### Indexes ###################################
def civil_index(request,url):
    comp = Compendium.objects.get(record_key=url)
    if comp.category == 'births':
        item_list = sanitize(GRObirth.objects.filter(compendium =comp.id).order_by('sort_date'))
    elif comp.category == 'deaths':
        item_list = GROdeath.objects.filter(compendium =comp.id).order_by('sort_date') 
    else:
        item_list = sanitize(GROmarriage.objects.filter(compendium =comp.id).order_by('sort_date')) 
    #for item in item_list:
    #    if item.person_id and item.person.private:
    #        item.person_id=0  

   
    context = {'item_list': item_list}
    return render(request, 'civilreg/{url}'.format(url=comp.template), context)

########### Certificates ###################################
def certificates(request, kind, item):
    comp = Compendium.objects.get(record_key=kind)
    if item == 'index':
        if kind == 'bcert':
            cert_list = BirthCertificate.objects.all().order_by('sort_date')
        elif kind== 'dcert':
            cert_list = Death_certificate.objects.all().order_by('date')
        else:
            cert_list = MarriageCertificate.objects.all().order_by('date')
        context = {'cert_list': cert_list}
        return render(request, 'civilreg/{url}'.format(url=comp.indextemplate), context)
    else:
        if kind== 'bcert':
            cert_details = BirthCertificate.objects.get(id=item)
        elif kind== 'dcert':
            cert_details = Death_certificate.objects.get(id=item)
        else:
            cert_details = MarriageCertificate.objects.get(id=item)
        return render(request, 'civilreg/{url}'.format(url=comp.template), {'cert_record': cert_details})


