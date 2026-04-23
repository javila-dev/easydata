from django.urls import path
from useraccounts import views


urlpatterns = [
    path("login/",views.account_login),
    path("passwordreset/",views.reset_password),
    path('logout/',views.account_logout),
    path('users/',views.usersadmin),
    path('resendwelcomemail',views.resend_welcome_mail),
]