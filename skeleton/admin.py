from django.contrib import admin

# Register your models here.

from .models import Menu, Compendium

admin.site.register(Menu)
admin.site.register(Compendium)
