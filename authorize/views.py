from django.shortcuts import render, redirect
from django.views import View
from .models import OrganizerUser, AttenderUser, EmailConfirmation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import AttenderSignupForm, OrganizerSignupForm
from django.contrib.auth.models import Group
from eEvent import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

import logging
import uuid

log = logging.getLogger(__name__)


class OrganizerSignup(View):
    def get(self, req):
        if req.user.is_authenticated:
            return redirect("event_index")
        form = OrganizerSignupForm()
        return render(req, "auth/organizer_signup.html", {"form": form})

    def post(self, req):
        form = OrganizerSignupForm(req.POST)
        message = "invalid data entered"
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                is_active = not settings.isEmailConfirmation
                user = User.objects.create_user(
                    username=username,
                    email=form.cleaned_data["email"],
                    password=password,
                    first_name=form.cleaned_data["firstName"],
                    last_name=form.cleaned_data["lastName"],
                    is_active=is_active
                )
                attenderGroup = Group.objects.get(name='AUTH_ORGANIZER')
                user.groups.add(attenderGroup)
                user.save()
                user = User.objects.latest("id")
                organizerUser = OrganizerUser(
                    user=user, phone=form.cleaned_data["phone"])
                organizerUser.save()
                log.info(f"Organizer signup success: {organizerUser.id}")
                return doLogin(req, username, password)
            except Exception as e:
                message = str(e)
            log.error(f"Organizer signup failed: {message}")
            return render(req, "auth/organizer_signup.html", {"form": form, "status": "fail", "message": message})


class AttenderSignup(View):
    def get(self, req):
        if req.user.is_authenticated:
            return redirect("event_index")
        form = AttenderSignupForm()
        return render(req, "auth/attender_signup.html", {"form": form})

    def post(self, req):
        form = AttenderSignupForm(req.POST)
        message = "invalid data entered"
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                is_active = not settings.isEmailConfirmation
                user = User.objects.create_user(
                    username=username,
                    email=form.cleaned_data["email"],
                    password=password,
                    first_name=form.cleaned_data["firstName"],
                    last_name=form.cleaned_data["lastName"],
                    is_active=is_active
                )
                attenderGroup = Group.objects.get(name='AUTH_ATTENDER')
                user.groups.add(attenderGroup)
                user.save()
                user = User.objects.latest("id")
                attenderUser = AttenderUser(
                    user=user, phone=form.cleaned_data["phone"], multiple=False)
                attenderUser.save()
                log.info(f"Attender signup success: {attenderUser.id}")
                return doLogin(req, username, password)
            except Exception as e:
                message = str(e)
        log.error(f"Attender signup failed: {message}")
        return render(req, "auth/attender_signup.html", {"form": form, "status": "fail", "message": message})


class Login(View):
    def get(self, req):
        if req.user.is_authenticated:
            return redirect("index")
        return render(req, "auth/login.html", {})

    def post(self, req):
        username = req.POST["username"]
        password = req.POST["password"]
        return doLogin(req, username, password)


def doLogin(req, username, password):
    authenticatedUser = authenticate(username=username, password=password)
    try:
        if not authenticatedUser:
            user = User.objects.filter(username=username)
            if user[0] and not user[0].is_active:
                raise Exception("Email is not verified")
            raise Exception("Failed to authenticate, maybe wrong username or password")
        login(req, authenticatedUser)
        log.info(f"Login success: {username}")
        return redirect("index")
    except Exception as e:
        log.info(f"Login failed for {username}: {str(e)}")
        return render(req, "auth/login.html", {"status": "fail", "message": str(e)})


class ExpiredException(Exception):
    pass

class Logout(View):
    def get(self, req):
        if req.user.is_authenticated:
            return render(req, "auth/logout.html")
        else:
            return redirect("auth_login")

    def post(self, req):
        logout(req)
        log.info("Logout success")
        return redirect("auth_login")
