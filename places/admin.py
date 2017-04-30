from django.contrib import admin

# Register your models here.
from .models import Country, County, Place

class PlaceAdmin(admin.ModelAdmin):
    search_fields = ['town']
    filter_horizontal = ('see_also',)

admin.site.register(Country)
admin.site.register(County)
admin.site.register(Place, PlaceAdmin)
