from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import *
from .serializers import *
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views import View
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from dal import autocomplete
from rest_framework import viewsets,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import *
import requests

apikey = '3d50abec-7071-4c24-9de8-fb29fb5b5d39'
languages = ['en', 'fr']

def AnalyseSoftware(software):
    session = requests.session()
    params = {'cpeMatchString' : software.cpe.reference, 'apiKey' : apikey}
    response = session.get('https://services.nvd.nist.gov/rest/json/cves/1.0/', params=params)
    cve_items = response.json()["result"]['CVE_Items']
    for cve_item in cve_items:
        description = cve_item['cve']['description']['description_data'][0]['value']
        score = cve_item['impact']['baseMetricV3']['cvssV3']['baseScore']
        severity = cve_item['impact']['baseMetricV3']['cvssV3']['baseSeverity']
        name = cve_item['cve']['CVE_data_meta']['ID']
        link = 'https://nvd.nist.gov/vuln/detail/' + name
        Vulnerability.objects.get_or_create(name=name, description=description, score=score, severity=severity, link=link, cpe=software.cpe)

class CPEAutocomplete(LoginRequiredMixin,autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CPE.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class GroupsViewSet(LoginRequiredMixin,viewsets.ModelViewSet):
    search_fields = ['id','name','description','slug']
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    filterset_fields = ['id','name','description','slug']
    serializer_class = GroupSerializer
    lookup_field = ('slug')

    def get_queryset(self):
        return self.request.user.extension.groups.all()

    def create(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid() and self.get_permissions():
            serializer.save(extension=request.user.extension)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get_permissions(self):
        if self.action in ['list','retrieve','create']:
            self.permission_classes = [IsAuthenticated,]
        elif self.action in ['update', 'partial_update','destroy']:
            self.permission_classes = [IsGroupOwner,]
        return super().get_permissions()

class AssetsViewSet(LoginRequiredMixin,viewsets.ModelViewSet):
    search_fields = ['id','name','description','slug']
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    filterset_fields = ['id','name','description','slug']
    serializer_class = AssetSerializer
    lookup_field = ('slug')

    def get_queryset(self):
        return self.request.user.extension.getassets().filter(group__slug=self.kwargs['group_slug'])

    def create(self, request, group_slug):
        group = request.user.extension.groups.get(slug=group_slug)
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid() and self.get_permissions():
            serializer.save(group=group)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get_permissions(self):
        if self.action in ['list','retrieve','create']:
            self.permission_classes = [IsAuthenticated,]
        elif self.action in ['update', 'partial_update','destroy']:
            self.permission_classes = [IsAssetOwner,]
        return super().get_permissions()

class SoftwareViewSet(LoginRequiredMixin,viewsets.ModelViewSet):
    search_fields = ['id','name','description','version','cpe','slug']
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    filterset_fields = ['id','name','description','version','cpe','slug']
    serializer_class = SoftwareSerializer
    lookup_field = ('slug')

    def get_queryset(self):
        return self.request.user.extension.getsoftwares().filter(asset__slug=self.kwargs['asset_slug'])

    def create(self, request, group_slug, asset_slug):
        asset = request.user.extension.getassets().get(slug=asset_slug)
        serializer = SoftwareSerializer(data=request.data)
        if serializer.is_valid() and self.get_permissions():
            serializer.save(asset=asset)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get_permissions(self):
        if self.action in ['list','retrieve','create']:
            self.permission_classes = [IsAuthenticated,]
        elif self.action in ['update', 'partial_update','destroy']:
            self.permission_classes = [IsSoftwareOwner,]
        return super().get_permissions()

class VulnerabilityViewSet(LoginRequiredMixin,viewsets.ModelViewSet):
    search_fields = ['id','name','description','score','severity','link','slug']
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    filterset_fields = ['id','name','description','score','severity','link','slug']
    lookup_field = ('slug')
    serializer_class = VulnerabilitySerializer
    http_method_names = ['get']

    def get_queryset(self):
        if self.kwargs.get('software_slug',None) :
            return self.request.user.extension.getsoftwares().get(slug=self.kwargs['software_slug']).getvulnerabilities()
        elif self.kwargs.get('asset_slug',None) :
            return self.request.user.extension.getassets().get(slug=self.kwargs['asset_slug']).getvulnerabilities()
        elif self.kwargs.get('group_slug') :
            return self.request.user.extension.groups.get(slug=self.kwargs['group_slug']).getvulnerabilities()
    
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes = [IsAuthenticated,]
        return super().get_permissions()

class Login(LoginView):
    template_name = 'Login.html'

class SignUp(SuccessMessageMixin, generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'Registration.html'
    success_message = "Your profile was created successfully"

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            return super().get(request)

class Home(LoginRequiredMixin, View):
    template_name='Home.html'

    def get(self, request):
        data = {'homenav' : True,'available_languages': languages}
        return render(request, self.template_name, data)

class Groups(LoginRequiredMixin, View):
    template_name='Groups.html'

    def get(self, request):
        groupform = GroupForm()
        assetform = AssetForm(user=request.user)
        data = {'groupnav' : True,'available_languages': languages,'groupform' : groupform,'assetform': assetform}
        return render(request, self.template_name, data)
    
    def post(self, request):
        if "groupform" in request.POST:
            groupform = GroupForm(request.POST)
            if groupform.is_valid():
                group_add = groupform.save(commit=False)
                group_add.extension = request.user.extension
                group_add.save()
                messages.success(request, _("Group created !"))
                return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, _("Invalid group form !"))
                return HttpResponseRedirect(request.path_info)
        elif "deletegroup" in request.POST:
            group_list = request.POST.getlist('groupcheck')
            for group in group_list:
                group_to_delete = request.user.extension.groups.get(pk=group)
                group_to_delete.delete()
            if len(group_list) > 1:
                messages.success(request, _("Successfully deleted "+str(len(group_list))+" groups !"))
            else:
                messages.success(request, _("Group deleted !"))
            return HttpResponseRedirect(request.path_info)
        elif "assetform" in request.POST:
            assetform = AssetForm(request.POST,user=request.user)
            if assetform.is_valid():
                asset_add = assetform.save(commit=False)
                asset_add.save()
                messages.success(request, _("Asset created !"))
                return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, _("Invalid asset form !"))
                return HttpResponseRedirect(request.path_info)
        elif "deleteasset" in request.POST:
            asset_list = request.POST.getlist('assetcheck')
            for asset in asset_list:
                asset_to_delete = request.user.extension.getassets().get(pk=asset)
                asset_to_delete.delete()
            if len(asset_list) > 1:
                messages.success(request, _("Successfully deleted "+str(len(asset_list))+" assets !"))
            else:
                messages.success(request, _("Asset deleted !"))
            return HttpResponseRedirect(request.path_info)

class AdminPanel(LoginRequiredMixin, View):
    template_name='Admin.html'

    def get(self, request):
        if request.user.is_superuser:
            data = {'adminnav': True,'available_languages': languages}
            return render(request, self.template_name, data)
        else:
            return HttpResponseRedirect('/')

class GroupProfile(LoginRequiredMixin, View):
    template_name='GroupProfile.html'

    def get(self, request, groupslug):
        group = Group.objects.get(slug=groupslug)
        if group in request.user.extension.groups.all():
            assetform = AssetForm()
            groupform = GroupForm(instance=group)
            softwareform = SoftwareForm(group=group)
            data = {'available_languages': languages, 'groupform': groupform, 'assetform': assetform, 'group': group, 'softwareform': softwareform}
            return render(request, self.template_name, data)
        else:
            return HttpResponseRedirect(request.path_info)

    def post(self, request, groupslug):
        group = Group.objects.get(slug=groupslug)
        if group in request.user.extension.groups.all():
            if "groupform" in request.POST:
                groupform = GroupForm(request.POST, instance=group)
                if groupform.is_valid():
                    group_update = groupform.save()
                    messages.success(request, _("Group updated !"))
                    return HttpResponseRedirect(request.path_info)
                else:
                    messages.error(request, _("Invalid group form !"))
                    return HttpResponseRedirect(request.path_info)
            elif "assetform" in request.POST:
                assetform = AssetForm(request.POST)
                if assetform.is_valid():
                    asset_add = assetform.save(commit=False)
                    asset_add.group = group
                    asset_add.save()
                    messages.success(request, _("Asset added !"))
                    return HttpResponseRedirect(request.path_info)
                else:
                    messages.error(request, _("Invalid asset form !"))
                    return HttpResponseRedirect(request.path_info)
            elif "deleteasset" in request.POST:
                asset_list = request.POST.getlist('assetcheck')
                for asset in asset_list:
                    asset_to_delete = request.user.extension.getassets().get(pk=asset)
                    asset_to_delete.delete()
                if len(asset_list) > 1:
                    messages.success(request, _("Successfully deleted "+str(len(asset_list))+" assets !"))
                else:
                    messages.success(request, _("Asset deleted !"))
                return HttpResponseRedirect(request.path_info)
            elif "deletegroup" in request.POST:
                group.delete()
                messages.success(request, _("Group deleted !"))
                return redirect('groups')
            elif "softwareform" in request.POST:
                softwareform = SoftwareForm(request.POST, group=group)
                if softwareform.is_valid():
                    softwareform.save()
                    messages.success(request, _("Software added !"))
                    return HttpResponseRedirect(request.path_info)
                else:
                    messages.error(request, _("Invalid software form !"))
                    return HttpResponseRedirect(request.path_info)
            elif "deletesoftware" in request.POST:
                software_list = request.POST.getlist('softwarecheck')
                for software in software_list:
                    software_to_delete = request.user.extension.getsoftwares().get(pk=software)
                    software_to_delete.delete()
                if len(software_list) > 1:
                    messages.success(request, _("Successfully deleted "+str(len(software_list))+" software !"))
                else:
                    messages.success(request, _("Software deleted !"))
                return HttpResponseRedirect(request.path_info)

class AssetProfile(LoginRequiredMixin, View):
    template_name='AssetProfile.html'

    def get(self, request, groupslug, assetslug):
        group = Group.objects.get(slug=groupslug)
        if group in request.user.extension.groups.all():
            asset = Asset.objects.get(slug=assetslug)
            assetform = AssetForm(instance=asset,user=request.user)
            softwareform = SoftwareForm()
            data = {'available_languages': languages, 'assetform': assetform, 'softwareform': softwareform, 'asset': asset}
            return render(request, self.template_name, data)
        else:
            return HttpResponseRedirect(request.path_info)

    def post(self, request, groupslug, assetslug):
        group = Group.objects.get(slug=groupslug)
        if group in request.user.extension.groups.all():
            asset = Asset.objects.get(slug=assetslug)
            if "assetform" in request.POST:
                assetform = AssetForm(request.POST, instance=asset)
                if assetform.is_valid():
                    asset_update = assetform.save()
                    messages.success(request, _("Asset updated !"))
                    return HttpResponseRedirect(request.path_info)
                else:
                    messages.error(request, _("Invalid asset form !"))
                    return HttpResponseRedirect(request.path_info)
            elif "softwareform" in request.POST:
                softwareform = SoftwareForm(request.POST)
                if softwareform.is_valid():
                    software_add = softwareform.save(commit=False)
                    software_add.asset = asset
                    software_add.save()
                    messages.success(request, _("Software added !"))
                    return HttpResponseRedirect(request.path_info)
                else:
                    messages.error(request, _("Invalid software form !"))
                    return HttpResponseRedirect(request.path_info)
            elif "deletesoftware" in request.POST:
                software_list = request.POST.getlist('softwarecheck')
                for software in software_list:
                    software_to_delete = request.user.extension.getsoftwares().get(pk=software)
                    software_to_delete.delete()
                if len(software_list) > 1:
                    messages.success(request, _("Successfully deleted "+str(len(software_list))+" software !"))
                else:
                    messages.success(request, _("Software deleted !"))
                return HttpResponseRedirect(request.path_info)
            elif "deleteasset" in request.POST:
                asset.delete()
                messages.success(request, _("Asset deleted !"))
                return redirect('groupprofile', groupslug=group.slug)

class SoftwareProfile(LoginRequiredMixin, View):
    template_name='SoftwareProfile.html'

    def get(self, request, groupslug, assetslug, softwareslug):
        group = Group.objects.get(slug=groupslug)
        if group in request.user.extension.groups.all():
            software = Software.objects.get(slug=softwareslug)
            softwareform = SoftwareForm(instance=software,group=group)
            data = {'available_languages': languages, 'softwareform': softwareform, 'software': software}
            return render(request, self.template_name, data)
        else:
            return HttpResponseRedirect(request.path_info)

    def post(self, request, groupslug, assetslug, softwareslug):
        group = Group.objects.get(slug=groupslug)
        if group in request.user.extension.groups.all():
            software = Software.objects.get(slug=softwareslug)
            if "softwareform" in request.POST:
                softwareform = SoftwareForm(request.POST, instance=software)
                if softwareform.is_valid():
                    software_update = softwareform.save()
                    messages.success(request, _("Software updated !"))
                    return HttpResponseRedirect(request.path_info)
                else:
                    messages.error(request, _("Invalid software form !"))
                    return HttpResponseRedirect(request.path_info)
            elif "deletesoftware" in request.POST:
                software.delete()
                messages.success(request, _("Software deleted !"))
                return redirect('assetprofile', groupslug=group.slug, assetslug=software.asset.slug)
            elif "analysesoftware" in request.POST:
                AnalyseSoftware(software)
                messages.success(request, _("Software analysed !"))
                return HttpResponseRedirect(request.path_info)

class VulnerabilityProfile(LoginRequiredMixin, View):
    template_name='VulnerabilityProfile.html'

    def get(self, request, vulnerabilityslug):
        vulnerability = Vulnerability.objects.get(slug=vulnerabilityslug)
        if vulnerability in request.user.extension.getvulnerabilities():
            data = {'available_languages': languages,'vulnerability': vulnerability}
            return render(request, self.template_name, data)