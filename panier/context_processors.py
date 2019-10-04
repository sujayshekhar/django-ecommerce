# -*- coding: utf-8 -*-
# Context processors

from .panier import Panier

# On instancie le panier à l'aide d'une requête et
# On le rend disponile pour les modèles comme une variable
# nommée ici panier


def panier(request):
    return {'panier': Panier(request)}

# Recuperation de l'adresse IP de l'user
def get_client_ip(request):
    return {'ip': request.META['REMOTE_ADDR']}
