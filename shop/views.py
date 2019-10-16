# -*- coding: utf-8 -*-

from django.db.models import Avg, Count, Max, Min
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categorie, Produit
from panier.forms import AjouterProduitPanierForm
from django.core.paginator import Paginator
from django.views.decorators.http import condition, require_http_methods
from shop.setlang import strip_language


# from .recommender import Recommender

# Creation des vues de notre catalogue
# Vue pour les recherches sur le site
@require_http_methods(["GET"])
def search(request):
    next_lang = strip_language(request.path)
    categories = Categorie.objects.all()
    produits = Produit.objects.filter(disponible=True)
    try:
        q = request.GET.get('q')
    except:
        q = None

    if q:
        produits = produits.filter(name__icontains=q)
    else:
        return redirect('shop:search')

    if not produits.exists():
        produits = produits.filter(categorie__name__icontains=q)

    context = {'query': q, 'produits': produits, 'categories': categories, 'next':next_lang}
    template = 'shop/produit/resultat.html'

    return render(request, template, context)


# Vue pour lister tous les produits
def all_produit(request, category_slug=None):
    next_lang = strip_language(request.path)
    categorie = None
    categories = Categorie.objects.all()
    produits = Produit.objects.filter(disponible=True)
    if category_slug:
        categorie = get_object_or_404(Categorie, slug=category_slug)
        produits = produits.filter(produits__name__in=categorie)

    context = {'category': categorie, 'categories': categories, 'produits': produits, 'next': next_lang}
    template = 'shop/produit/shop_listing.html'

    return render(request, template, context)


# Vue pour les details des produits
@require_http_methods(["GET"])
def detail_produit(request, id, slug):
    next_lang = strip_language(request.path)
    produit = get_object_or_404(Produit, id=id, slug=slug, disponible=True)
    categories = produit.categorie.filter()
    page_title = produit.name
    meta_keywords = produit.meta_keywords
    meta_description = produit.meta_description

    # Similar products
    product_cat_ids = produit.categorie.values_list('id')
    similar_products = Produit.objects.filter(categorie__in=product_cat_ids).exclude(id=produit.id).annotate(Count("categorie", distinct=True)).order_by()[:6]

    formulaire_panier_produit = AjouterProduitPanierForm(auto_id='id_%s')
    # r = Recommender()
    # recommended_products = r.suggest_products_for([produit], 4)
    template = 'shop/produit/shop_detail.html'
    context = {'produit': produit, 'categories':categories, 'similar_products': similar_products, 'formulaire_panier_produit': formulaire_panier_produit,
        'page_title' : page_title, 'meta_keywords' : meta_keywords, 'meta_description' : meta_description,
        'next': next_lang}

    return render(request, template, context)


# Vue pour lister toutes les categories de produits
def all_categorie(request):
    next_lang = strip_language(request.path)
    page_title = 'categorie'
    categories = Categorie.objects.all()
    produits = Produit.objects.filter(disponible=True)

    context = {'categories': categories, 'produits': produits,
        'page_title' : page_title, 'next': next_lang }
    template = 'shop/produit/shop_all_cat.html'

    return render(request, template, context)

# Vue pour lister tous les produits par categorie
def liste_categorie(request, category_slug=None):
    next_lang = strip_language(request.path)
    categorie = None
    categories = Categorie.objects.all()
    produits = Produit.objects.filter(disponible=True)
    if category_slug:
        categorie = get_object_or_404(Categorie, slug=category_slug)
        produits = produits.filter(categorie=categorie)
        page_title = categorie.name
        meta_keywords = categorie.meta_keywords
        meta_description = categorie.meta_description

    context = {'produits': produits, 'page_title' : page_title, 'meta_keywords' : meta_keywords,
        'meta_description' : meta_description, 'next': next_lang}
    template = 'shop/produit/shop_list_cat.html'

    return render(request, template, context)
