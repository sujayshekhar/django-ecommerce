# -*- coding: utf-8 -*-
"""
    commandes URL Configuration
"""
from django.utils.translation import gettext_lazy as _
from django.urls import path
from . import views as commande

app_name = 'commandes'

urlpatterns = [
    path(_('create/'), commande.creer_commande, name="commander"),
    path(_('admin/commande/<int:id_commande>/'), commande.detail_commande_admin,
         name='detail_commande_admin'),
    path(_('admin/commande/<int:id_commande>/pdf/'), commande.pdf_commande_admin,
         name='pdf_commande_admin'),
]
