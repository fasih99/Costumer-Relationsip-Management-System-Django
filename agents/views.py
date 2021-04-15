import random
from django.shortcuts import render,reverse,redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView,
                                 ListView,
                                 DeleteView,
                                 UpdateView,
                                 DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentCreateForm
from .mixins import OrganizerAndLoginRequiredMixin
from django.core.mail import send_mail
# Create your views here.

class AgentListView(OrganizerAndLoginRequiredMixin, ListView):
    template_name = 'leads/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        agent_organization = self.request.user.userprofile
        return Agent.objects.filter(organization=agent_organization)
    

class AgentCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name="leads/agent_create.html"
    model = Agent
    form_class = AgentCreateForm

    def form_valid(self,form):
        user = form.save(commit=False)
        user.set_password(f"{random.randint(0,10000000)}")
        user.is_agent = True
        user.is_organizer = False
        user.save()

        Agent.objects.create( 
            user = user,
            organization = self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an Agent",
            message ="You were added as agent on CRM.",
            from_email="admin@test.com",
            recipient_list=[user.email,]
        )
        return super(AgentCreateView,self).form_valid(form)


    def get_success_url(self):
        return reverse('agents:agent_list')

class AgentDetailView(OrganizerAndLoginRequiredMixin,DetailView):
    template_name="leads/agent_detail.html"
    context_object_name = 'agent'
    
    def get_queryset(self):
        agent_organization = self.request.user.userprofile
        return Agent.objects.filter(organization=agent_organization)

class AgentUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name="leads/agent_update.html"
    form_class = AgentCreateForm
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse('agents:agent_detail')

    def get_queryset(self):
        agent_organization = self.request.user.userprofile
        return Agent.objects.filter(organization=agent_organization)


class AgentDeleteView(OrganizerAndLoginRequiredMixin,DeleteView):
    template_name="leads/agent_delete.html"
    form_class= AgentCreateForm
    context_object_name = 'agent'
    success_url = reverse_lazy('agents:agent_list')
    
    def get_queryset(self):
        agent_organization = self.request.user.userprofile
        return Agent.objects.filter(organization=agent_organization)
   