from django.contrib import admin

# Register your models here.
from .models import GRObirth, BirthCertificate, GROdeath, GROmarriage, MarriageCertificate, Death_certificate


class McertAdmin(admin.ModelAdmin):
	#list_filter =('group',)
	filter_horizontal = ('witnesses',)
   
class DcertAdmin(admin.ModelAdmin):
	#list_filter =('group',)
	filter_horizontal = ('other_people',) 

admin.site.register(GRObirth)
admin.site.register(BirthCertificate)
admin.site.register(GROmarriage)
admin.site.register(MarriageCertificate, McertAdmin)
admin.site.register(GROdeath)
admin.site.register(Death_certificate, DcertAdmin)
