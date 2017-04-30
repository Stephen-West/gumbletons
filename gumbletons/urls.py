"""gumbletons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from skeleton.views import index, compendium
from civilreg.views import civil_index,  certificates
from parish.views import burial_list, baptism_list, marriage_list
from streetsurveys.views import rolls_index, rolls_year , R1939index, census
from people.views import show_person, people_index, gumbleton_index, nongumbleton_index, allpeople, public_people, private_people
from snippets.views import miscellaneous_index, miscellaneous_item
from plainpages.views import renderpage
from utilities.views import admin_check, record_book,index_book, census_book, pid_check
from places.views import show_place

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^experimental/allpeople.html$', allpeople),
    url(r'^experimental/recordbook.html$', record_book),
    url(r'^experimental/indexbook.html$', index_book),
    url(r'^experimental/censusbook.html$', census_book),
    url(r'^private/publicpeople.html$', public_people),
    url(r'^private/privatepeople.html$', private_people),
    url(r'^private/admin_check.html$', admin_check),
    url(r'^private/pid_check.html$', pid_check),
#Level 0 pages
    url(r'^records_index.html$', compendium),
    url(r'^(\w+\.html$)', renderpage),
    url(r'^(general/project.html)$', renderpage),
    url(r'^(general/about_robert_gumbleton.html)$', renderpage),
    url(r'^(general/useful_links.html)$', renderpage),
#indexes
	url(r'^peopleindexes/allpeople.html$', people_index), 
	url(r'^peopleindexes/gumbletons.html$', gumbleton_index), 
	url(r'^peopleindexes/nongumbletons.html$', nongumbleton_index), 
#Indexes for all level 1 groups    
    url(r'^(\w*)/index.html$', index),
    url(r'^parish/baptisms/index.html$', baptism_list),
    url(r'^parish/burials/index.html$', burial_list),
    url(r'^parish/marriages/index.html$', marriage_list),

#Civil registration
    url(r'^civilreg/(.*births).html$', civil_index),
    url(r'^civilreg/(.*deaths).html$', civil_index),
    url(r'^civilreg/(.*marriages).html$', civil_index),
    url(r'^civilreg/(.*cert)/(.*).html$', certificates),

#Census etc
    url(r'^census/r1939.html$', R1939index),
	url(r'^census/(\w*).html$', census),
    url(r'^staterecords/electoralrolls/index.html$', rolls_index),
    url(r'^staterecords/electoralrolls/(\w*).html$', rolls_year),  
 
    url(r'^places/(\w*).html$', show_place),
    url(r'^people/(\w*).html$', show_person),
    url(r'^(\w*)/(\w*)/index.html$', miscellaneous_index),
    url(r'^(\w*)/(\w*)/(\w+).html$', miscellaneous_item),
]  
