# -*- coding: utf-8 -*-

""" Shop url configuration"""
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from shop.sitemaps import CatSitemaps
from . import views

sitemaps = {
    'cat': CatSitemaps,
}

app_name = 'shop'

urlpatterns = (
    path('', views.all_produit, name='all_produit'),
    path(_('search/'), views.search, name='search'),
    path(_('shop/category/'), views.all_categorie, name='all_categorie'),
    path(_('shop/category/<slug:category_slug>/'), views.liste_categorie, name='listing_categorie'),
    path(_('shop/category/<slug:category_slug>/'), views.all_produit, name='all_produit_par_categorie'),
    path(_('shop/product/<slug:slug>/<int:id>/'), views.detail_produit, name='detail_produit'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
)
