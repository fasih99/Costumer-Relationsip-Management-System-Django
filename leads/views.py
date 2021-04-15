from django.shortcuts import render,redirect,reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Lead,Agent,Category
from .forms import (create_form,
                   leadsModelForm,
                   LeadsUser,
                   AssignAgentForm,
                   leadsCategoryForm)
from django.views.generic import ( TemplateView,
                                   DetailView,
                                   CreateView,
                                   ListView,
                                   DeleteView,
                                   UpdateView,
                                   FormView)
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizerAndLoginRequiredMixin
from django.core.mail import send_mail

# Create your views here.

class LeadsListView(LoginRequiredMixin, ListView):
    template_name = 'leads/leads_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        queryset = Lead.objects.all()
        user = self.request.user
        
        if self.request.user.is_agent:
            #finding all leads of all agents in the oraganization agent belongs to 
            queryset = queryset.filter(organization=user.agent.organization)
            #finding all leads of the agent which matches the current user
            queryset = queryset.filter(agent__user=self.request.user)

        else:
            #finding all leads belonging to the oraganization of User
            queryset = queryset.filter(organization=user.userprofile, agent__isnull=False)
            

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        queryset = Lead.objects.all()

        if user.is_organizer:
            queryset = queryset.filter(organization=user.userprofile, agent__isnull=True)
            context.update({
                'unassigned_leads': queryset,
            })
        return context
    


class SignUp(CreateView):
    template_name = "registration/signUp.html"
    form_class = LeadsUser

    def get_success_url(self):
        return reverse_lazy("login")


def leads_view(request):
    # return HttpResponse("<h1>Hello World!<h1>")
    leads = Lead.objects.all()
    context = { "leads" : leads}
    return render(request, 'leads/leads_list.html', context)

class Home(TemplateView):
    template_name = "home.html"
    context_object_name = 'user'

def home(request):
    return render(request,'home.html')

class LeadsDetailView(LoginRequiredMixin,DetailView):
    template_name='leads/leads_detail.html'
    queryset = Lead.objects.all()
    context_object_name = 'leads'

    def get_queryset(self):
        queryset = Lead.objects.all()
        user = self.request.user
        
        if self.request.user.is_agent:
            #finding all leads of all agents in the oraganization agent belongs to 
            queryset = queryset.filter(organization=user.agent.oraganization)
            #finding all leads of the agent which matches the current user
            queryset = queryset.filter(agent__user=self.request.user)

        else:
            #finding all leads belonging to the oraganization of User
            queryset = queryset.filter(organization=user.userprofile)
            

        return queryset


def leads_detail(request, pk):
    leads=Lead.objects.get(id=pk)
    context = {
        'leads':leads
    }
    return render(request,'leads/leads_detail.html', context)

class LeadsCreateView(OrganizerAndLoginRequiredMixin,CreateView):
    template_name = 'leads/leads_create.html'
    form_class = leadsModelForm

    def get_queryset(self):
        queryset = Lead.objects.all()
        user = self.request.user
        #finding all leads belonging to the oraganization of User
        queryset = queryset.filter(organization=user.userprofile)
        return queryset

    
    def form_valid(self,form):
        lead = form.save(commit=False)
        user = self.request.user
        lead.organization = user.userprofile


        send_mail( 
            subject = "A lead has been created ",
            message = "Go to the site to see the new lead",
            from_email = "test@test.com",
            recipient_list = ["test2@test.com"]
        )
        # send email
        return super(LeadsCreateView, self).form_valid(form)


    def get_success_url(self):
        return reverse("leads:leads_list")


def leads_create(request):
    form=leadsModelForm()
    if request.method=='POST':
        print("Receiving Post!")
        form = leadsModelForm(request.POST)
    
        if form.is_valid():
           form.save()
           return redirect("/leads")
      
        
    context={
        'form': form
    }
    return render(request,'leads/leads_create.html',context)

class LeadsUpdateView(OrganizerAndLoginRequiredMixin,UpdateView):
    template_name = 'leads/leads_update.html'
   
    form_class = leadsModelForm
    context_object_name = 'leads'

    def get_queryset(self):
        queryset = Lead.objects.all()
        user = self.request.user
        #finding all leads belonging to the oraganization of User
        queryset = queryset.filter(organization=user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse_lazy('leads:leads_detail', kwargs = {'pk':self.get_object().id})


def leads_update(request,pk):
    lead = Lead.objects.get(id=pk)
    form = leadsModelForm(instance=lead)
    if request.method == 'POST':
        form = leadsModelForm(request.POST,instance=lead)
        form.save()
        return redirect("/leads")
    context={
        "leads":lead,
        "form":form
    }
    return render(request,'leads/leads_update.html', context)

class LeadsDeleteView(OrganizerAndLoginRequiredMixin,DeleteView):
    template_name='leads/leads_delete.html'
    form_class = leadsModelForm
    context_object_name = 'leads'

    def get_queryset(self):
        queryset = Lead.objects.all()
        user = self.request.user
        #finding all leads belonging to the oraganization of User
        queryset = queryset.filter(organization=user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse_lazy('leads:leads_list')


def leads_delete(request,pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")


class AssignAgentFormView(OrganizerAndLoginRequiredMixin,FormView):
    template_name = "leads/assign_agents.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs = super(AssignAgentFormView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request':self.request,
        })
        return kwargs
        

    def get_success_url(self):
        return reverse("leads:leads_list")

    def form_valid(self,form):
        agent=form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent=agent
        lead.save()
        return super(AssignAgentFormView,self).form_valid(form)


class CategoryList(LoginRequiredMixin,ListView):
    template_name= "leads/category_list.html"
    context_object_name = 'cats'

    def get_queryset(self):
        queryset = Category.objects.all()
        user = self.request.user

        if user.is_organizer :
            queryset = queryset.filter(organization=user.userprofile)
        else:
            queryset = queryset.filter(organization=user.agent.organization)
          
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        queryset = Lead.objects.all()

        if user.is_organizer :
            queryset = queryset.filter(organization=user.userprofile)
        else:
            queryset = queryset.filter(organization=user.agent.organization)
          
        context.update({
            'uncategorized_leads_count': queryset.filter(category__isnull=True).count(),
        })

        return context


class CategoryDetailView(LoginRequiredMixin,DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = 'cats'

    def get_queryset(self):
        queryset = Category.objects.all()
        user = self.request.user

        if user.is_organizer :
            queryset = queryset.filter(organization=user.userprofile)
        else:
            queryset = queryset.filter(organization=user.agent.organization)
          
        return queryset

class LeadCategoryUpdate(LoginRequiredMixin,UpdateView):
    template_name = 'leads/category_update.html'
    context_object_name = 'leads'
    form_class = leadsCategoryForm



    def get_queryset(self):
        queryset = Lead.objects.all()
        user = self.request.user
        
        if self.request.user.is_agent:
            #finding all leads of all agents in the oraganization agent belongs to 
            queryset = queryset.filter(organization=user.agent.oraganization)
            #finding all leads of the agent which matches the current user
            queryset = queryset.filter(agent__user=self.request.user)

        else:
            #finding all leads belonging to the oraganization of User
            queryset = queryset.filter(organization=user.userprofile)
            

        return queryset

    def get_success_url(self):
            return reverse_lazy('leads:leads_detail', kwargs = {'pk':self.get_object().id})

# def leads_create(request):
#     form=create_form()
#     if request.method=='POST':
#         print("Receiving Post!")
#         form = create_form(request.POST)
    
#         if form.is_valid():
#            print(form.cleaned_data)
#            f_name=form.cleaned_data['f_name']
#            l_name=form.cleaned_data['l_name']
#            age=form.cleaned_data['age']
#            agent=Agent.objects.first()
#            Lead.objects.create(
#               f_name=f_name,
#               l_name=l_name,
#               age=age ,
#               agent=agent,
#            )
#            print("New lead created")
#            return redirect("/leads")
      
        
#     context={
#         'form': form
#     }
#     return render(request,'leads/leads_create.html',context)
   