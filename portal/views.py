from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
import requests
from .models import HashUserToken
import uuid
from django.contrib import messages


api_key = "c9ef2a2e-806a-11e9-ade6-0200cd936042"

#
# def register(request):
#     form = UserCreationForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             phone = request.POST['phone']
#             return HttpResponse("User Created")
#     else:
#         return render(request, 'portal/register.html', {'form': form})
#


def otp_input(request):
    print(request.session.items())
    if request.method == "POST":
        user_otp = request.POST['otp']
        url = "http://2factor.in/API/V1/{0}/SMS/VERIFY/{1}/{2}".format(api_key, request.session['otp_session_data'], user_otp)
        response = requests.request("GET", url)
        data = response.json()
        hash_user_token = HashUserToken.objects.get(uuid=request.session["hash_user_token_uuid"])
        user = hash_user_token.user
        if data['Status'] == "Success":
            user.is_active = True
            user.save()
            del request.session['hash_user_token_uuid']
            del request.session['otp_session_data']
            hash_user_token.delete()
            print(request.session.items())
            return HttpResponse("Sucess Verified {}".format(user.username))
        else:
            messages.warning(request, "please enter correct OTP!")
    return render(request, "portal/otp_input.html")


def register(request):
    print(request.session.items())
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
            hash_token = HashUserToken.objects.create(user=user, variable_2fa=data['Details'])
            request.session["hash_user_token_uuid"] = str(hash_token.uuid)
            return redirect("portal:otp_input")

    else:
        return render(request, 'portal/register.html', {'form': form})


