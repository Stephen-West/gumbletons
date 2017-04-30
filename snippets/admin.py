from django.contrib import admin
from snippets.models import    Snippet

# Register your models here.



class GenealogyAdmin(admin.ModelAdmin):
    filter_horizontal = ('other_names',)
    

class SnippetAdmin(admin.ModelAdmin):
    list_filter =('group',)
    filter_horizontal = ('other_names',)
    search_fields = ['name', 'title']
    

admin.site.register(Snippet, SnippetAdmin)
