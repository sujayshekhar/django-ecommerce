# -*- coding: utf-8 -*-

"""
    Panier URL configuration
"""
from django.utils.translation import gettext_lazy as _
from django.urls import path
from . import views as panier_views

app_name = 'panier'

urlpatterns = [
    path('', panier_views.detail_panier, name="detail_panier"),
    path(_('add/<int:id_produit>/'), panier_views.ajout_panier, name="ajout_panier"),
    path(_('remove/<int:id_produit>/'), panier_views.enlever_panier, name="enlever_panier"),
]
