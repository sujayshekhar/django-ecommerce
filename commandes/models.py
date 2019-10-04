from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from coupons.models import Coupon
from shop.models import Produit


# Medeles pour l'enregistrement des commandes des clients

class Commande(models.Model):
    coupon = models.ForeignKey(Coupon, related_name="Commandes", null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    email = models.EmailField(_('email'))
    adresse = models.CharField(_('adress'), max_length=250)
    telephone = models.CharField(_('phone number'), max_length=8)
    ville = models.CharField(_('city'), max_length=100)
    creer = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    payer = models.BooleanField(_('paid'), default=True)
    discount = models.IntegerField(_('discount'), default=0, validators=[MinValueValidator(0),
        MaxValueValidator(100)])
    # table de paiement
    id_braintree = models.CharField(_('ID'), blank=True, max_length=50)

    class Meta:
        ordering = ('-creer',)
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return 'Commande {}'.format(self.id)

    def get_depense_total(self):
        depense_total = sum(item.get_depense() for item in self.items.all())
        return depense_total - depense_total * (self.discount / Decimal('100'))


class ItemCommande(models.Model):
    commande = models.ForeignKey(Commande, related_name='items', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, related_name='items_commande', on_delete=models.CASCADE)
    prix = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField(_('Quantity'), default=1)

    class Meta:
        verbose_name = "Element Commandé"
        verbose_name_plural = "Elements Commandés"

    def __str__(self):
        return f"{ self.quantite } of {self.commande.id}"

    def get_depense(self):
        return self.prix * self.quantite
