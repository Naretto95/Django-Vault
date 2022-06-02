from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from sqlalchemy import false
from .forms import *
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views import View
from django.utils.translation import gettext as _

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
        assets = Asset.objects.filter(group__in=request.user.extension.groups.all())
        softwares = Software.objects.filter(asset__in=assets)
        vulnerabilities = Vulnerability.objects.filter(software__in=softwares)
        data = {'homenav' : True,'available_languages': ['en', 'fr'],'vulnerabilities': vulnerabilities,'assets': assets,'softwares': softwares}
        return render(request, self.template_name, data)

class Groups(LoginRequiredMixin, View):
    template_name='Groups.html'

    def get(self, request):
        groupform = GroupForm()
        data = {'groupnav' : True,'available_languages': ['en', 'fr'],'groupform' : groupform }
        return render(request, self.template_name, data)
    
    def post(self, request):
        if "groupform" in request.POST:
            groupform = GroupForm(request.POST)
            if groupform.is_valid():
                group_add = groupform.save(commit=False)
                group_add.extension = request.user.extension
                group_add.save()
                request.user.extension.groups.add(group_add)
                messages.success(request, _("Group created !"))
                return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, _("Invalid group form !"))
                return HttpResponseRedirect(request.path_info)
        elif "deletegroup" in request.POST:
            group_list = request.POST.getlist('groupcheck')
            for group in group_list:
                group_to_delete = Group.objects.get(pk=group)
                group_to_delete.delete()
            if len(group_list) > 1:
                messages.success(request, _("Successfully deleted "+str(len(group_list))+" groups !"))
            else:
                messages.success(request, _("Group deleted !"))
            return HttpResponseRedirect(request.path_info)

class AdminPanel(LoginRequiredMixin, View):
    template_name='Admin.html'

    def get(self, request):
        if request.user.is_superuser:
            data = {'adminnav': True,'available_languages': ['en', 'fr']}
            return render(request, self.template_name, data)
        else:
            return HttpResponseRedirect('/')