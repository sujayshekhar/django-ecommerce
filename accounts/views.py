# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from accounts.forms import RegisterForm
from shop.setlang import strip_language


# Create your views here.

def register_request(request):
    next_lang = strip_language(request.path)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            # redirect to profile compte:
            return redirect('accounts:profile')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            context = { 'form':form }
            template = 'accounts/accounts_register.html'
            return render(request, template, context)

    form = RegisterForm()

    context = {'form': form, 'next': next_lang}
    template = 'accounts/accounts_register.html'

    return render(request, template, context)


def login_request(request):
    next_lang = strip_language(request.path)
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as { username }")
                # redirect to profile compte:
                return redirect('accounts:profile')
            else:
                return redirect('accounts:login')
        else:
            return redirect('accounts:login')

    form = AuthenticationForm()

    context = { 'form': form, 'next_lang': next_lang }
    template = 'accounts/accounts_login.html'

    return render(request, template, context)


def profile(request):
    next_lang = strip_language(request.path)
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    return render(request, 'accounts/accounts_profile.html', { 'next': next_lang })
