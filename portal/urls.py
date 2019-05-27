from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

app_name = "portal"

urlpatterns = [
    url(r"^register/$", views.register, name='register'),
    url(r'^otp_input/$', views.otp_input, name='otp_input')

]
