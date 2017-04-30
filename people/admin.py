from django.contrib import admin

# Register your models here.

from .models import Person, Spouse





class PersonAdmin(admin.ModelAdmin):
    search_fields = ['names', 'surname', 'PID']
class SpouseAdmin(admin.ModelAdmin):
    search_fields = ['man__surname', 'woman__surname', 'woman__names', 'man__names', 'woman__PID', 'man__PID']

admin.site.register(Person, PersonAdmin)
admin.site.register(Spouse, SpouseAdmin)
