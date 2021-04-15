from django import forms
from .models import Lead, User,Agent
from django.contrib.auth.forms import UserCreationForm,UsernameField


class leadsModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        exclude = ['organization']

class leadsCategoryForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )



class create_form(forms.Form):
    f_name= forms.CharField()
    l_name=forms.CharField()
    age=forms.IntegerField(min_value=0)

class LeadsUser(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

        
class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self,*args,**kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organization=request.user.userprofile)
        super(AssignAgentForm,self).__init__(*args,**kwargs)
        self.fields['agent'].queryset=agents



