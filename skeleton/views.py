from django.shortcuts import render

# Create your views here.

from .models import Menu, Compendium

def index(request,m):
    this_menu = Menu.objects.get(path = m)
    #index_list = Compendium.objects.order_by('sequence').filter(group = this_group.id)
    index_list = []
    #check for submenus
    #submenus = Menu.objects.filter(parent = this_menu.id)
    #recursive submenus left for another day
    compendiums = Compendium.objects.filter(parent = this_menu.id)
    for comp in compendiums:
        #print ("One found", comp.name, comp.url)
        record={}
        record['title']=comp.name
        record['url']= '/{p}/{u}'.format(p=m, u=comp.url)
        index_list.append(record)
    #print (index_list)
    context =  {'menu' : this_menu , 'index_list' : index_list}
    return render(request, 'skeleton/index.html', context)

def compendium(request):
	#if request.user.is_authenticated():
	c_list = Compendium.objects.filter(index=True)
	#else:
	#	c_list = Compendium.objects.filter(index=True, private=False)
	return render(request, 'skeleton/compendium.html', {'c_list' : c_list})
