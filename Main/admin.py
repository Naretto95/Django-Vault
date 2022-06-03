from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.register(Software)
admin.site.register(Vulnerability)
admin.site.register(Group)
admin.site.register(Asset)
admin.site.register(Extension)

class CPEResource(resources.ModelResource):

    class Meta:
        model = CPE
        exclude = ('id')
        import_id_fields = ('name','reference')


class CPEAdmin(ImportExportModelAdmin):
    resource_class = CPEResource

admin.site.register(CPE,CPEAdmin)
