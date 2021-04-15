from django import forms
from leads.models import Agent
from django.contrib.auth import get_user_model

User = get_user_model()

class AgentCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields= (
                'email',
                'username',
                'first_name',
                'last_name',
                )
