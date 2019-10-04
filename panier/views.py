# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Produit
from .panier import Panier
from .forms import AjouterProduitPanierForm
from coupons.forms import CouponForm
from shop.recommender import Recommender

from shop.setlang import strip_language


# Create your views here.

@require_POST
def ajout_panier(request, id_produit):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=id_produit)
    formulaire = AjouterProduitPanierForm(request.POST)
    if formulaire.is_valid():
        effacer_donnee = formulaire.cleaned_data
        panier.ajout(
            produit=produit,
            quantite=effacer_donnee['quantite'],
            update_quantite=effacer_donnee['update'])
    return redirect('panier:detail_panier')


def enlever_panier(request, id_produit):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=id_produit)
    panier.enlever(produit)
    return redirect('panier:detail_panier')

def detail_panier(request):
    next_lang = strip_language(request.path)
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    panier = Panier(request)
    for item in panier:
        item['form_update_quantite'] = AjouterProduitPanierForm(
            initial={'quantite': item['quantite'], 'update': True})
    # On ajout le coupon au panier
    appliquer_le_coupon = CouponForm()

    # r = Recommender()
    # panier_pruduit = [item['produit'] for item in panier]
    # recommande_produit = r.suggest_products_for(panier_pruduit, max_results=4)
    context = {'panier': panier, 'appliquer_le_coupon':appliquer_le_coupon, 'next': next_lang}
    return render(request, 'panier/detail.html', context)
