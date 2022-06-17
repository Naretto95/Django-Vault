from django.contrib.admin import AdminSite
from django.urls import path,include
from django.conf import settings
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class MyAdminSite(AdminSite):
    site_header = 'Vault Administration'
    site_title = 'Vault'

admin_site = MyAdminSite()
admin_site.register(Software)
admin_site.register(Vulnerability)
admin_site.register(Group)
admin_site.register(Asset)
admin_site.register(Extension)

class CPEResource(resources.ModelResource):

    class Meta:
        model = CPE
        exclude = ('id')
        import_id_fields = ('name','reference')


class CPEAdmin(ImportExportModelAdmin):
    resource_class = CPEResource

admin_site.register(CPE,CPEAdmin)
