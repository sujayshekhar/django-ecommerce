# -*- coding: utf-8 -*-

from django.db.models import Count
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
    try:
        produits = Produit.objects.all()
        categories = Categorie.objects.all()
        q = request.GET.get('q')
    except:
        q = None
        categorie = None
        produits = None

    if not q:
        return redirect('shop:liste_produit')

    else:
        produits = Produit.objects.filter(name__icontains=q)
        context = {'query':q, 'produits':produits, 'categories':categories, 'next':next_lang}
        template = 'shop/produit/resultat.html'

    if not produits.exists():
        produits = Produit.objects.filter(categorie__name__icontains=q)
        context = {'produits':produits, 'categories':categories, 'next':next_lang}
        template = 'shop/produit/resultat.html'

    return render(request, template, context)


# Vue pour lister tous les produits
def liste_produit(request, category_slug=None):
    next_lang = strip_language(request.path)
    categorie = None
    categories = Categorie.objects.all().order_by("-creation")
    produits = Produit.objects.filter(disponible=True)
    if category_slug:
        categorie = get_object_or_404(Categorie, slug=category_slug)
        produits = produits.filter(categorie=categorie)
    return render(request, 'shop/produit/listing.html',
        {
            'category':categorie, 'categories':categories,
            'produits':produits, 'next':next_lang
        })

def cat_filter(request, category_slug):
    next_lang = strip_language(request.path)
    categories = Categorie.objects.all()
    produits = Produit.objects.filter(disponible=True)
    if category_slug:
        categorie = get_object_or_404(Categorie, slug=category_slug)
        produits = produits.filter()
    context = {'category':categorie, 'categories':categories, 'produits':produits, 'next':next_lang}
    template = 'shop/produit/cat_listing.html'
    return render(request, template, context)


# Vue pour les details des produits
@require_http_methods(["GET"])
def detail_produit(request, id, slug):
    next_lang = strip_language(request.path)
    username = request.GET.get('username', None)
    user = None
    if username:
        try:
            user = User.objects.get(username=username)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            pass
    if user:
        return Produit.objects.filter(user=user)
    else:
        produit = get_object_or_404(Produit, id=id, slug=slug, disponible=True)
    produit = get_object_or_404(Produit, id=id, slug=slug, disponible=True)
    formulaire_panier_produit = AjouterProduitPanierForm(auto_id='id_%s')
    # r = Recommender()
    # recommended_products = r.suggest_products_for([produit], 4)
    template = 'shop/produit/detail.html'
    context = {'produit':produit, 'formulaire_panier_produit':formulaire_panier_produit, 'next':next_lang}
    return render(request, template, context)


# Vue pour lister les categories de produits
def list_categorie(request):
    next_lang = strip_language(request.path)
    category = Categorie.objects.all()
    paginator = Paginator(category, 20)
    page = request.GET.get('page')
    cat = paginator.get_page(page)
    return render(request, "shop/produit/cat_listing.html", {'cat':cat, 'next':next_lang})
