# -*- coding: utf-8 -*-
# Context processors

from ecommerce import settings

from .panier import Panier
from shop.models import Marque, Categorie



# On instancie le panier à l'aide d'une requête et
# On le rend disponile pour les modèles comme une variable
# nommée ici panier


def panier(request):
    return {'panier': Panier(request)}


# Recuperation de l'adresse IP de l'user
def get_client_ip(request):
    return {'ip': request.META['REMOTE_ADDR']}


def ecommerce(request):
    return {
        'active_categories': Categorie.objects.filter(is_active=True),
        'active_marques': Marque.objects.filter(is_active=True),
        'site_name': settings.SITE_NAME,
        'site_desc' : settings.SITE_DESCRIPTION,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'request': request
    }
