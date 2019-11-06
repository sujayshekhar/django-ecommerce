# -*- coding: utf-8 -*-

from decimal import Decimal
from django.conf import settings

from shop.models import Produit
from coupons.models import Coupon


class Panier(object):
    """ docstring for panier """

    def __init__(self, request):
        """ Initialisation du panier """
        self.session = request.session
        panier = self.session.get(settings.PANIER_SESSION_ID)
        if not panier:
            # Enregistre un panier vide dans la session
            panier = self.session[settings.PANIER_SESSION_ID] = {}
        self.panier = panier

        # On stocke le coupon du jour
        self.id_coupon = self.session.get('id_coupon')

    def ajout(self, produit, quantite=1, update_quantite=False):
        """ Ajouter un produit au panier ou mettre a jour son panier"""
        id_produit = str(produit.id)
        if id_produit not in self.panier:
            self.panier[id_produit] = {'quantite': 0, 'prix': str(produit.prix)}

        if update_quantite:
            self.panier[id_produit]['quantite'] = quantite
        else:
            self.panier[id_produit]['quantite'] += quantite
        self.save()

    def save(self):
        # marque la session comme modifiee pour qu'elle soit enregistrer
        self.session[settings.PANIER_SESSION_ID] = self.panier
        self.session.modified = True

    def enlever(self, produit):
        """ La méthode enlever() supprime un produit donné du dictionnaire du panier
        et appelle la méthode save() pour mettre à jour le panier dans la session."""
        id_produit = str(produit.id)
        if id_produit in self.panier:
            del self.panier[id_produit]
            self.save()

    def __iter__(self):
        """ On Itére sur les articles dans le panier et
        jusqu'à obtenir tous les produits de la base de données."""
        ids_produit = self.panier.keys()

        # On récupérer les objets produits et les ajoute au panier
        produits = Produit.objects.filter(id__in=ids_produit)
        panier = self.panier.copy()
        for produit in produits:
            panier[str(produit.id)]['produit'] = produit

        for item in panier.values():
            item['prix'] = Decimal(item['prix'])
            item['prix_total'] = item['prix'] * item['quantite']
            yield item

    def __len__(self):
        """ On profile tous les items dans le panier """
        return sum(item['quantite'] for item in self.panier.values())


    # On calcule le coût total des articles dans le panier
    def get_cout_total(self):
        return sum(Decimal(item['prix']) * item['quantite'] for item in self.panier.values())

    # Enfin on efface la session
    def clear_session(self):
        # effacer les paniers de la session
        del self.session[settings.PANIER_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.id_coupon:
            return Coupon.objects.get(id=self.id_coupon)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_cout_total()
        return Decimal('0')

    def get_cout_total_apres_discount(self):
        return self.get_cout_total() - self.get_discount()
