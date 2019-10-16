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
    slug = models.SlugField(max_length=200, unique=True, help_text='Unique value for product page URL, created from name.')
    meta_keywords = models.CharField('Meta Keywords', max_length=200, help_text="Comma-delimited set of SEO keywords for meta tag")
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:listing_categorie', args=[self.slug])

    @property
    def get_cat_count(self):
        return Produit.objects.filter(categorie__name__icontains=self.name).count()

    class Meta:
        db_table = 'categories'
        ordering = ('-name',)
        verbose_name = 'categorie'
        verbose_name_plural = 'categories'

class Pub(models.Model):
    """docstring for Pub"""
    categorie = models.ManyToManyField(Categorie)
    name = models.CharField("Pub name", max_length=200, db_index=True)
    pub = models.ImageField("pub image", upload_to='produits/pub/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Publicité'


class Produit(models.Model):
    """ Definition des params du produits :
    nom, description, image, prix, disponibilite """

    categorie = models.ManyToManyField(Categorie)
    name = models.CharField("Nom du produit", max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True,
        help_text='Unique value for product page URL, created from name.')
    description = HTMLField("Description du produit", null=True, blank=True)

    prix = models.DecimalField("Prix de vente", max_digits=10, decimal_places=2)
    prix_reduit = models.DecimalField("Prix promo", max_digits=10, decimal_places=2, blank=True, null=True)

    image = models.ImageField("Ajouter une image", upload_to='produits/img/%Y/%m/%d', blank=True)

    disponible = models.BooleanField("Disponibilité", default=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, null=True, blank=True)
    is_bestseller = models.BooleanField(default=False)

    meta_keywords = models.CharField(max_length=255,
        help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255,
        help_text='Content for description meta tag')

    creation = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField("Ajouté le", auto_now_add=False, default=datetime.datetime.now)

    def __str__(self):
        return self.name

    @property
    def view_product_count(self):
        return Produit.objects.filter(name=self.name).count()


    def get_absolute_url(self):
        return reverse('shop:detail_produit', args=[self.slug, self.id])

    class Meta:
        ordering = ['-name', '-creation']
        verbose_name = 'produit'
        verbose_name_plural = 'produits'
        index_together = (('id', 'slug'),)
