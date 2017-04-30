from django.contrib import admin

# Register your models here.
from .models import Address,ElectoralRolls, household1939, individual, Census, Household

class R1939Inline(admin.TabularInline):
	model=individual

class censusInline(admin.TabularInline):
	model=Census
	
class RollAdmin(admin.ModelAdmin):
    search_fields = ['names', 'surname']

class HouseholdAdmin(admin.ModelAdmin):
    inlines = [R1939Inline, ]

class CensHouseholdAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [censusInline, ]

class CensusAdmin(admin.ModelAdmin):
    search_fields = ['name']

class Ind1939Admin(admin.ModelAdmin):
    search_fields = ['names','surname']

admin.site.register(ElectoralRolls, RollAdmin)
admin.site.register(Address)
admin.site.register(Census, CensusAdmin)
admin.site.register(Household, CensHouseholdAdmin)
admin.site.register(household1939, HouseholdAdmin)
admin.site.register(individual, Ind1939Admin)
