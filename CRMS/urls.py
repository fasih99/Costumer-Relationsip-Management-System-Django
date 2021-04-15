import debug_toolbar
from django.contrib import admin
from django.urls import path,include
from leads.views import home,Home,SignUp
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (LoginView,
                                      LogoutView,
                                      PasswordResetView,
                                      PasswordResetDoneView,
                                      PasswordResetConfirmView,
                                      PasswordResetCompleteView)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/',include(debug_toolbar.urls)),
    path('',Home.as_view(),name='home'),
    path('agents/',include('agents.urls',namespace='agents')),
    path('leads/',include('leads.urls',namespace='leads')),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('signUp/',SignUp.as_view(),name='signUp'),
    path('password-reset-done',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset-password/',PasswordResetView.as_view(),name='password_reset'),
    path('reset-password/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password_reset_form'), 
    path('reset-complete',PasswordResetCompleteView.as_view(),name='password_reset_complete')

  
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
