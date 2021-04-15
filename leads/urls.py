from django.urls import path,include
from .views import ( LeadsUpdateView,
                     LeadsDeleteView, 
                     LeadsListView,
                     LeadsDetailView,
                     LeadsCreateView,
                     SignUp,
                     AssignAgentFormView,
                     CategoryList,
                     CategoryDetailView,
                     LeadCategoryUpdate)
from django.contrib.auth.views import LoginView


app_name='leads'

urlpatterns = [
    path('',LeadsListView.as_view(), name="leads_list"),
    path('<int:pk>/',LeadsDetailView.as_view(), name="leads_detail"),
    path('<int:pk>/update/',LeadsUpdateView.as_view(), name="leads_update"),
    path('<int:pk>/delete/',LeadsDeleteView.as_view(), name="leads_delete"),
    path('<int:pk>/assign/',AssignAgentFormView.as_view(), name="leads_assign"),
    path('<int:pk>/category_update/',LeadCategoryUpdate.as_view(), name="category_update"),
    path('category_detail/<int:pk>',CategoryDetailView.as_view(),name='category_detail'),

    path('login/',LoginView.as_view(),name='login'),
    path('create/',LeadsCreateView.as_view(), name="leads_create"),

    path('category_list',CategoryList.as_view(),name='category_list'),

    

]


    
