from django.contrib import admin
from .models import Burial, Baptism, Marriage
# Register your models here.

admin.site.register(Burial)
admin.site.register(Baptism)
admin.site.register(Marriage)
