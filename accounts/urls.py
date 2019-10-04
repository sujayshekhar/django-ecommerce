# -*- coding: utf-8 -*-

""" Shop url configuration"""
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views


app_name = 'accounts'

urlpatterns = (
     path(_('register/'), accounts_views.register, name='register'),

     path(_('profile/'), accounts_views.profile, name='profile'),

     path(_('login/'), auth_views.LoginView.as_view(
          template_name="accounts/login.html"), name='login'),

     path(_('logout/'), auth_views.LogoutView.as_view(
          template_name="shop/produit/listing.html"), name='logout'),

     path(_('password-reset/'), auth_views.PasswordResetView.as_view(
          template_name="accounts/password_reset.html",
          email_template_name="accounts/password_reset_email.html",
          success_url="/accounts/password_reset_done/"), name="password_reset"),

     path(_('password-reset/done/'), auth_views.PasswordResetDoneView.as_view(
          template_name="accounts/password_reset_done.html"),
          name="password_reset_done"),

     path(_('password-reset-confirm/<uidb64>/<token>/'),
          auth_views.PasswordResetConfirmView.as_view(
          template_name="accounts/password_reset_email.html"),
          name="password_reset_confirm"),

     path(_('password-reset-complete/'),
          auth_views.PasswordResetCompleteView.as_view(
          template_name="accounts/password_reset_complete.html"),
          name="password_reset_complete"),
)
