# Vue pour la recommandation d'articles similaires
import redis
from django.conf import settings
from .models import Produit


# Connexion a redis : on lance le server redis avant
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommender(object):
    """docstring for Recommender"""
    
    @staticmethod
    def get_product_key(self, id):
        return 'product:{}:purchased_with'.format(id)
    
    # on cherche les autres produits achetés avec chaque produit
    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(self.get_product_key(str[product_id]), with_id, amount=1)
    
    def suggest_products_for(self, products, max_results=6):
        # Class de suggesstion des produits
        product_ids = [p.id for p in products]
        if len(products) == 1:
            suggestions = r.zrange(self.get_product_key(self, product_ids[0]),
                                   0, -1, desc=True)[:max_results]
        else:
            # on genere une clé temporaire
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            
            # Ensuite on affiche plusieurs produits combiner des scores de tous les
            # produits et on stocke l'ensemble des resultats trié dans une clé temporaire
            keys = [self.get_product_key(self, id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            
            # On supprime les identifiants des produits pouur lesquels
            # la recommandation s'applique
            r.zrem(tmp_key, *product_ids)
            
            # on affiche les identifiants des produits par leur score, tri décroissant
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            
            # on supprime la clé temporaire
            r.delete(tmp_key)
        
        suggested_products_ids = [int(id) for id in suggestions]
        # on affiche enfin les produits suggérés en les triant par ordre d'apparition
        suggested_products = list(Produit.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        
        return suggested_products
    
    def clear_purchases(self):
        for id in Produit.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(self, id))
