from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import LogoutView
from rest_framework.schemas import get_schema_view
from rest_framework_nested import routers
from django.views.generic import TemplateView
from . import views

api = 'api/v1/'
router = routers.DefaultRouter()
router.register(r'groups', views.GroupsViewSet, basename="group")
group_router = routers.NestedSimpleRouter(router, r'groups', lookup='group')
group_router.register(r'assets', views.AssetsViewSet, basename='asset')
group_router.register(r'vulnerabilities', views.VulnerabilityViewSet, basename='vulnerability')
asset_router = routers.NestedSimpleRouter(group_router, r'assets', lookup='asset')
asset_router.register(r'softwares', views.SoftwareViewSet, basename='software')
asset_router.register(r'vulnerabilities', views.VulnerabilityViewSet, basename='vulnerability')
software_router = routers.NestedSimpleRouter(asset_router, r'softwares', lookup='software')
software_router.register(r'vulnerabilities', views.VulnerabilityViewSet, basename='vulnerability')

urlpatterns = [
    path(api, include(router.urls)),
    path(api, include(group_router.urls)),
    path(api, include(asset_router.urls)),
    path(api, include(software_router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', views.Home.as_view(),name="home"),
    path('groups/', views.Groups.as_view(),name="groups"),
    path('login/', views.Login.as_view(redirect_authenticated_user=True),name="login"),
    path('search/', views.Login.as_view(redirect_authenticated_user=True),name="search"),
    path('adminpanel/', views.AdminPanel.as_view(),name="adminpanel"),
    path('signup/', views.SignUp.as_view(),name="signup"),
    path('vulnerability/<str:vulnerabilityslug>/', views.VulnerabilityProfile.as_view(),name="vulnerabilityprofile"),
    path('groups/<str:groupslug>/', views.GroupProfile.as_view(),name="groupprofile"),
    path('groups/<str:groupslug>/<str:assetslug>/', views.AssetProfile.as_view(),name="assetprofile"),
    path('groups/<str:groupslug>/<str:assetslug>/<str:softwareslug>/', views.SoftwareProfile.as_view(),name="softwareprofile"),
    url(r'^openapi-schema', get_schema_view(title="Vault API",description="Vault",version="1.0.0",public=True,), name='openapi-schema'),
    url(r'docs/', TemplateView.as_view(template_name='swagger-ui.html',extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    url(r'^cpe-autocomplete/$',views.CPEAutocomplete.as_view(),name='cpe-autocomplete',),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]