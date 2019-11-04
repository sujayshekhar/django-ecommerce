# -*- coding: utf-8 -*-

import redis
from django.conf import settings
from .models import Produit


# Connexion a redis : on lance le server redis avant
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Recommender(object):
    """docstring for Recommender"""

    def get_produit_key(self, id):
        return 'produit:{}:purchased_with'.format(id)

    # on cherche les autres produits achetés avec chaque produit
    def produits_bought(self, produits):
        produit_ids = [p.id for p in produits]
        for produit_id in produit_ids:
            for with_id in produit_ids:
                if produit_id != with_id:
                    r.zincrby(self.get_produit_key(str[produit_id]), with_id, amount=1)

    def suggest_produits_for(self, produits, max_results=10):
        # Class de suggesstion des produits
        produit_ids = [p.id for p in produits]
        if len(produits) == 1:
            suggestions = r.zrange(self.get_produit_key(produit_ids[0]), 0, -1, desc=True)[:max_results]
        else:
            # on genere une clé temporaire
            flat_ids = ''.join([str(id) for id in produit_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)

            # Ensuite on affiche plusieurs produits combiner des scores de tous les
            # produits et on stocke l'ensemble des resultats trié dans une clé temporaire
            keys = [self.get_produit_key(id) for id in produit_ids]
            r.zunionstore(tmp_key, keys)

            # On supprime les identifiants des produits pouur lesquels
            # la recommandation s'applique
            r.zrem(tmp_key, *produit_ids)

            # on affiche les identifiants des produits par leur score, tri décroissant
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]

            # on supprime la clé temporaire
            r.delete(tmp_key)

        suggested_produits_ids = [int(id) for id in suggestions]
        # on affiche enfin les produits suggérés en les triant par ordre d'apparition
        suggested_produits = list(Produit.objects.filter(id__in=suggested_produits_ids))
        suggested_produits.sort(key=lambda x: suggested_produits_ids.index(x.id))

        return suggested_produits

    def clear_purchases(self):
        for id in Produit.objects.values_list('id', flat=True):
            r.delete(self.get_produit_key(id))
