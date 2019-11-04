# -*- coding: utf-8 -*-

"""
    Panier URL configuration
"""

from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views as views

app_name = 'panier'

urlpatterns = [
    path('', views.detail_panier, name="detail_panier"),
    path(_('panier/add/<int:id_produit>/'), views.ajout_panier, name="ajout_panier"),
    path(_('panier/remove/<int:id_produit>/'), views.enlever_panier, name="enlever_panier"),
]
