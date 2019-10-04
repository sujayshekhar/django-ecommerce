# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

# Definition du model Categorie

LABEL_CHOICES = (
    ('N', 'badge-new'),
    ('S', 'badge-sale'),
)


class Categorie(models.Model):
    """ Definition du model Categorie : nom et slug de la categorie """
    name = models.CharField("Type de produit", max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:liste_produit_par_categorie', args=[self.slug])

    def get_cat_url(self):
        return reverse('shop:listing_categorie', args=[self.slug])

    @property
    def get_produits(self):
        return Produit.objects.filter(categorie__name__icontains=self.name)

    @property
    def cat_count(self):
        return Categorie.objects.filter(name=self).count()

    class Meta:
        ordering = ('-name',)
        verbose_name = 'categorie'
        verbose_name_plural = 'categories'


class Produit(models.Model):
    """ Definition des params du produits :
    nom, description, image, prix, disponibilite """

    categorie = models.ForeignKey(Categorie, related_name='produits', on_delete="models.CASCADE")
    name = models.CharField("Nom du produit", max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    description = HTMLField("Description du produit", null=True, blank=True)

    prix = models.DecimalField("Prix de vente", max_digits=10, decimal_places=2)
    prix_reduit = models.DecimalField("Prix promo", max_digits=10, decimal_places=2, blank=True)

    image = models.ImageField("Ajouter une image", upload_to='produits/img/%Y/%m/%d', blank=True)
    thumbnails = models.ImageField("Autres image", upload_to='produits/thumb/%Y/%m/%d', blank=True)

    disponible = models.BooleanField("Disponibilité", default=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, null=True, blank=True)

    creation = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField("Ajouté le", auto_now_add=False, default=datetime.datetime.now)

    def __str__(self):
        return self.name

    @property
    def view_product_count(self):
        return Produit.objects.filter(name=self).count()

    def get_absolute_url(self):
        return reverse('shop:detail_produit', args=[self.slug, self.id])

    class Meta:
        ordering = ['-name', '-creation']
        verbose_name = 'produit'
        verbose_name_plural = 'produits'
        index_together = (('id', 'slug'),)