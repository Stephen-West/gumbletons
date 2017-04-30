from django.shortcuts import render
from utilities.privacy_filters import sanitize

# Create your views here.

from .models import Burial, Baptism, Marriage

def burial_list(request):
    burial_list = Burial.objects.order_by('sort_date')
    context = {'burial_list': burial_list}
    return render(request, 'burials/burials.html', context)

def baptism_list(request):
    baptism_list = sanitize(Baptism.objects.order_by('sort_date'))
    context = {'baptism_list': baptism_list}
    return render(request, 'baptisms/baptisms.html', context)

def marriage_list(request):
    marriage_list = sanitize(Marriage.objects.order_by('sort_date'))
    context = {'marriage_list': marriage_list}
    return render(request, 'marriages/marriages.html', context)
