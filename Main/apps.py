from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class AdminSiteConfig(AdminConfig):
    default_site = 'Main.admin.MyAdminSite'

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Main'
