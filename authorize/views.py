from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import AttenderSignupForm, OrganizerSignupForm, LoginForm


class OrganizerSignup(View):
    def get(self, req):
        form = OrganizerSignupForm()
        return render(req, "auth/organizer_signup.html", {"form": form})

    def post(self, req):
        form = OrganizerSignupForm(req.POST)
        if form.is_valid():
            form.save()
            print(f"signup success\n{form.cleaned_data}")
            return doLogin(req, form)
        
        print(f"signup failed\n{form}")
        return render(req, "auth/organizer_signup.html", {"form": form, "status": "failed"})


class AttenderSignup(View):
    def get(self, req):
        form = AttenderSignupForm()
        return render(req, "auth/attender_signup.html", {"form": form})

    def post(self, req):
        form = AttenderSignupForm(req.POST)
        if form.is_valid():
            form.save()
            print(f"signup success\n{form.cleaned_data}")
            return doLogin(req, form)
        print(f"signup failed\n{form}")
        return render(req, "auth/attender_signup.html", {"form": form, "status": "failed"})


class Login(View):
    def get(self, req):
        form = LoginForm()
        return render(req, "auth/login.html", {"form": form})

    def post(self, req):
        form = LoginForm(req.POST)
        if form.is_valid():
            return doLogin(req, form)



def doLogin(req, form):
    username = form.cleaned_data["username"]
    password = form.cleaned_data["password"]
    authenticatedUser = authenticate(username=username, password=password)
    if authenticatedUser:
        login(req, authenticatedUser)
        print(f"login success\n{form.cleaned_data["username"]}")
        return redirect("event_index")
    else:
        return render(req, "auth/login.html", {"form": form, "status": "failed"})

class Logout(View):
    def get(self, req):
        if req.user.is_authenticated:
            return render(req, "auth/logout.html")
        else:
            return redirect("auth_login")

    def post(self, req):
        logout(req)
        return HttpResponse("Logout successful!")