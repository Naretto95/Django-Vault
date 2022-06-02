from django import forms
from .models import *

class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ['name','description','version']
        widgets = {'description': forms.TextInput(attrs={'size': 20})}

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name','description']
        widgets = {'description': forms.TextInput(attrs={'size': 20})}

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name','description']
        widgets = {'description': forms.TextInput(attrs={'size': 50})}