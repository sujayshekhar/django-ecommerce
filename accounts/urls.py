# -*- coding: utf-8 -*-

""" Shop url configuration"""
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views


app_name = 'accounts'

urlpatterns = (
    path(_('register/'), accounts_views.register_request, name='register'),
    path(_('profile/'), accounts_views.profile, name='profile'),
    path(_('login/'), accounts_views.login_request, name='login'),
    path(_('logout/'), auth_views.LogoutView.as_view(
        template_name="shop/produit/shop_listing.html"), name='logout'),
)
