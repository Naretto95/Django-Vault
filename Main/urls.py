from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.Home.as_view(),name="home"),
    path('groups/', views.Groups.as_view(),name="groups"),
    path('login/', views.Login.as_view(redirect_authenticated_user=True),name="login"),
    path('search/', views.Login.as_view(redirect_authenticated_user=True),name="search"),
    path('adminpanel/', views.AdminPanel.as_view(),name="adminpanel"),
    path('signup/', views.SignUp.as_view(),name="signup"),
    path('groups/<str:groupslug>/', views.GroupProfile.as_view(),name="groupprofile"),
    path('groups/<str:groupslug>/<str:assetslug>/', views.AssetProfile.as_view(),name="assetprofile"),
    path('groups/<str:groupslug>/<str:assetslug>/<str:softwareslug>/', views.SoftwareProfile.as_view(),name="softwareprofile"),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]