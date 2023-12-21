from django.shortcuts import render, redirect
from django.views import View
from .models import OrganizerUser, AttenderUser
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import AttenderSignupForm, OrganizerSignupForm


class OrganizerSignup(View):
    def get(self, req):
        form = OrganizerSignupForm()
        return render(req, "auth/organizer_signup.html", {"form": form})

    def post(self, req):
        form = OrganizerSignupForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                username=username,
                email=form.cleaned_data["email"],
                password=password,
                first_name=form.cleaned_data["firstName"],
                last_name=form.cleaned_data["lastName"]
            )
            user.save()
            user = User.objects.latest("id")
            organizerUser = OrganizerUser(user=user, phone=form.cleaned_data["phone"])
            organizerUser.save()
            print(f"signup success: {form.cleaned_data}")
            return doLogin(req, username, password)
        print(f"signup failed: {form.cleaned_data}")
        return render(req, "auth/organizer_signup.html", {"form": form, "status": "failed"})


class AttenderSignup(View):
    def get(self, req):
        form = AttenderSignupForm()
        return render(req, "auth/attender_signup.html", {"form": form})

    def post(self, req):
        form = AttenderSignupForm(req.POST)
        if form.is_valid(): 
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                username=username,
                email=form.cleaned_data["email"],
                password=password,
                first_name=form.cleaned_data["firstName"],
                last_name=form.cleaned_data["lastName"]
                )
            user.save()
            user = User.objects.latest("id")
            attenderUser = AttenderUser(user=user, phone=form.cleaned_data["phone"], multiple=form.cleaned_data["multiple"])
            attenderUser.save()
            print(f"signup success: {form.cleaned_data}")
            return doLogin(req, username, password)
        print(f"signup failed: {form.cleaned_data}")
        return render(req, "auth/attender_signup.html", {"form": form, "status": "failed"})


class Login(View):
    def get(self, req):
        return render(req, "auth/login.html", {})

    def post(self, req):
        return doLogin(req)



def doLogin(req, username, password):
    authenticatedUser = authenticate(username=username, password=password)
    if authenticatedUser:
        login(req, authenticatedUser)
        print(f"login success: {username}")
        return redirect("event_index")
    else:
        return render(req, "auth/login.html", {"status": "failed"})

class Logout(View):
    def get(self, req):
        if req.user.is_authenticated:
            return render(req, "auth/logout.html")
        else:
            return redirect("auth_login")

    def post(self, req):
        logout(req)
        return HttpResponse("Logout successful!")