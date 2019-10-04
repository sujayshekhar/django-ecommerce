from django.conf import settings
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from accounts.forms import RegisterForm
from shop.setlang import strip_language


# Create your views here.

def register(request):
    next_lang = strip_language(request.path)
    if request.user.is_authenticated:
        return redirect('accounts:logout')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                if user is not None and user.is_active:
                    login(request, user)
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            form = RegisterForm()

        return render(request, 'accounts/register.html', {'form': form, 'next': next_lang})

def profile(request):
    next_lang = strip_language(request.path)
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    return render(request, 'accounts/profile.html', { 'next': next_lang })
