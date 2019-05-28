from django.contrib.auth.forms import UserCreationForm
import requests
from .models import OtpSession
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib import messages
from django.conf import settings


api_key = settings.API_KEY_2FA


def otp_input(request):
    if request.method == "POST":
        user_otp = request.POST['otp']
        url = "http://2factor.in/API/V1/{0}/SMS/VERIFY/{1}/{2}".format(api_key, request.session['otp_session_data'], user_otp)
        response = requests.request("GET", url)
        data = response.json()
        otp_session = OtpSession.objects.get(uuid=request.session["otp_session_uuid"])
        user = otp_session.user
        if data['Status'] == "Success":
            user.is_active = True
            user.save()
            del request.session['otp_session_uuid']
            del request.session['otp_session_data']
            otp_session.delete()
            return HttpResponse("Sucess Verified {}".format(user.username))
        else:
            messages.warning(request, "please enter correct OTP!")
    return render(request, "portal/otp_input.html")


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            phone = request.POST['phone']
            url = "http://2factor.in/API/V1/{api_key}/SMS/{phone}/AUTOGEN/OTPSEND".format(api_key=api_key, phone=phone)
            response = requests.request("GET", url)
            data = response.json()
            request.session['otp_session_data'] = data['Details']
            hash_token = OtpSession.objects.create(user=user, data=data['Details'])
            request.session["otp_session_uuid"] = str(hash_token.uuid)
            return redirect("portal:otp_input")

    else:
        return render(request, 'portal/register.html', {'form': form})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'portal/home.html'
