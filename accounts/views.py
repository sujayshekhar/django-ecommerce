# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

from shop.setlang import strip_language
from accounts.forms import RegisterForm


# Create your views here.

def register_request(request):
    next_lang = strip_language(request.path)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            if user.is_active:
                messages.success(request, f"New account created: { user.pseudo }")
                login(request, user)
                # redirect to profile compte:
                return redirect('accounts:profile')
    else:
        form = RegisterForm()

    context = {'form': form, 'next': next_lang}
    template = 'accounts/accounts_register.html'

    return render(request, template, context)


def login_request(request):
    next_lang = strip_language(request.path)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, f"You are now logged in as { user.pseudo }")
                # redirect to profile compte:
                return redirect('accounts:profile')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()

    context = { 'form': form, 'next_lang': next_lang }
    template = 'accounts/accounts_login.html'

    return render(request, template, context)


def profile(request):
    next_lang = strip_language(request.path)
    if not request.user.is_authenticated and not request.user.is_active:
        return redirect('accounts:login')

    return render(request, 'accounts/accounts_profile.html', { 'next': next_lang })
