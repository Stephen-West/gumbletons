from django.shortcuts import render
from .models import Snippet
from skeleton.models import Compendium
from utilities.urlfilters import preparse
from utilities.privacy_filters import people_filter
# Create your views here.

def miscellaneous_index(request, u1, u2):
    """Various pages are serviced by the miscellaneous index.
    URLs are of the form /category/subcategory/index.html
    where 'category' is just windowdressing and 'subcategory' identifies 
    the particular group of miscellaneous items.
    
    First we have to find the relevant Compendium entry (table skeleton_compendiums) by matching the field 'record_key'
    """
    comp = Compendium.objects.get(record_key = u2)
    #print ('found' + comp.name)
    s_list = people_filter(Snippet.objects.filter(group = u2))
    #print (str(len(s_list)) + " records")
    title = comp.name
    index_template = 'snippets/miscellaneous_index.html'
    if comp.template:
        index_template = comp.template
    rubric = comp.rubric
    context = {'s_list': s_list, 'group_name' : title, 'compendium' : comp}
    return render(request, index_template, context)

def miscellaneous_item(request, u1, key, id):
    snippet = Snippet.objects.get(id = id)
    snippet.content=preparse(snippet.content)
    comp = Compendium.objects.get(record_key=key)
    context = {'snippet' : snippet, 'compendium' : comp}
    return render(request, 'snippets/snippet.html', context)
