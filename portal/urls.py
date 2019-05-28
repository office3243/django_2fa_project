from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import CustomLoginForm


app_name = "portal"

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(template_name='portal/login.html', authentication_form=CustomLoginForm),
        name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='portal/logout.html'), name='logout'),

    url(r"^register/$", views.register, name='register'),
    url(r'^otp_input/$', views.otp_input, name='otp_input')

]
