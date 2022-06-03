from django import forms
from .models import *

class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ['name','description','version']
        widgets = {'description': forms.TextInput(attrs={'size': 20})}

class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ['name','description','version','asset']
        widgets = {'description': forms.TextInput(attrs={'size': 20})}

    def __init__(self,*args,**kwargs):
        group = kwargs.pop('group', None)
        super(SoftwareForm,self).__init__(*args,**kwargs)
        if group :
            self.fields['asset'].queryset = group.assets.all()
        else :
            self.fields.pop("asset")

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name','description','group']
        widgets = {'description': forms.TextInput(attrs={'size': 20})}
    
    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user', None)
        super(AssetForm,self).__init__(*args,**kwargs)
        if user :
            self.fields['group'].queryset = user.extension.groups.all()
        else:
            self.fields.pop("group")

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name','description']
        widgets = {'description': forms.TextInput(attrs={'size': 50})}