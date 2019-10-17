# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db.models import Avg, Count, Max, Min
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from shop.setlang import strip_language

from shop.models import Categorie, Produit, Review, Cluster
from shop.forms import ReviewAdminForm

from panier.forms import AjouterProduitPanierForm
from .suggestions import update_clusters


# from .recommender import Recommender

# Creation des vues de notre catalogue
# Vue pour les recherches sur le site
@require_http_methods(["GET"])
def search(request):
    next_lang = strip_language(request.path)
    categories = Categorie.is_active.all()
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
    produits = Produit.objects.filter(disponible=True).prefetch_related('categorie')

    if category_slug:
        categorie = get_object_or_404(Categorie, slug=category_slug)
        produits = produits.filter(categorie__name__icontains='produits')

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

    #
    form = ReviewAdminForm()

    # Similar products
    product_cat_ids = produit.categorie.values_list('id')
    similar_products = Produit.objects.filter(
        categorie__in=product_cat_ids).exclude(id=produit.id).annotate(
        Count("categorie", distinct=True)).prefetch_related('categorie').order_by()[:6]

    # popular views products
    formulaire_panier_produit = AjouterProduitPanierForm(auto_id='id_%s')
    # r = Recommender()
    # recommended_products = r.suggest_products_for([produit], 4)
    template = 'shop/produit/shop_detail.html'
    context = {
        'produit': produit, 'categories':categories,
        'similar_products': similar_products,
        'formulaire_panier_produit': formulaire_panier_produit,
        'form': form,
        'page_title' : page_title, 'meta_keywords' : meta_keywords,
        'meta_description' : meta_description, 'next': next_lang
    }

    return render(request, template, context)


# Vue pour lister toutes les categories de produits
def all_categorie(request):
    next_lang = strip_language(request.path)
    page_title = 'categorie'
    categories = Categorie.objects.all()
    produits = Produit.objects.filter(disponible=True).prefetch_related('categorie')

    context = {'categories': categories, 'produits': produits,
        'page_title' : page_title, 'next': next_lang }
    template = 'shop/produit/shop_all_cat.html'

    return render(request, template, context)

# Vue pour lister tous les produits par categorie
def liste_categorie(request, category_slug=None):
    next_lang = strip_language(request.path)
    categorie = None
    categories = Categorie.objects.all()
    produits = Produit.objects.filter(disponible=True).prefetch_related('categorie')
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


# Review list views
def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date', 'rating')[:9]
    context = {'latest_review_list': latest_review_list}
    template = 'shop/produit/shop_review_list.html'

    return render(request, template, context)

# Review detail views
def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    context = { 'review': review }
    template = 'shop/produit/shop_review_detail.html'

    return render(request, template, context)

# add review views
def add_review(request, produit_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    produit = get_object_or_404(Produit, id=produit_id, disponible=True)

    form = ReviewAdminForm()

    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.produit = produit
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('shop:detail_produit', args=(produit.id,)))

    template = 'shop/produit/shop_review_detail.html'
    context = { 'produit': produit, 'form': form }

    return render(request, template, context)


def user_review_list(request, username=None):
    if not username:
        username = request.user.username

    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username': username}
    template = 'shop/produit/shop_user_review.html'

    return render(request, template, context)


def user_recommendation_list(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    # get request user reviewd product
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('produit')
    user_reviews_produit_ids = set(map(lambda x: x.produit.id, user_reviews))

    # get request user cluster name (just the first one righ now)
    try:
        user_cluster_name = User.objects.get(username=request.user.username).cluster.first().name
    except IndexError:
        # if no cluster has been assigned for a user, update clusters
        update_clusters()
        user_cluster_name = User.objects.get(username=request.user.username).cluster.first().name

    # get usernames for other members of the cluster
    user_cluster_other_members = Cluster.objects.get(name=user_cluster_name).users.exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get usernames for other members of the cluster
    other_users_reviews = Review.objects.filter(user_name__in=other_members_usernames).exclude(produit__id__in=user_reviews_produit_ids)
    other_user_reviews_produit_ids = set(map(lambda x: x.produit.id, other_users_reviews))

    # then get a wine list including the previous IDs, order by rating
    produit_list = sorted(list(Produit.objects.filter(id__in=other_user_reviews_produit_ids)),
        key=lambda x: x.average_rating, reverse=True
    )
    print(produit_list)

    context = { 'username': request.user.username, 'produit_list': produit_list }
    template = 'shop/produit/user_recommendation_list.html'

    return render(request, template, context)
