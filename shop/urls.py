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
    path('', views.liste_produit, name='liste_produit'),
    path(_('search/'), views.search, name='search'),
    path(_('shop/category/<slug:category_slug>/'), views.cat_filter, name='listing_categorie'),
    path(_('shop/category/<slug:category_slug>/'), views.liste_produit, name='liste_produit_par_categorie'),
    path(_('shop/product/<slug:slug>/<int:id>/'), views.detail_produit, name='detail_produit'),
    path(_('shop/category/'), views.list_categorie, name='list_categorie'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
)
