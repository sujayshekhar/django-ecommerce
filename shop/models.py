# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

import numpy as np
from tinymce.models import HTMLField

# Definition du model Categorie

LABEL_CHOICES = (
    ('N', 'badge-new'),
    ('S', 'badge-sale'),
)

class Marque(models.Model):
    name = models.CharField("Marque du produit", max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:listing_marques', args=[self.slug])

    @property
    def count(self):
        return Produit.objects.filter(marque__name=self).count()

    class Meta:
        ordering = ('-name',)
        verbose_name = 'marque'
        verbose_name_plural = 'marques'

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
    def count(self):
        return Produit.objects.filter(categorie__name=self).count()

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

@python_2_unicode_compatible
class Produit(models.Model):
    """ Definition des params du produits : nom, description, image, prix, disponibilite """

    marque = models.ForeignKey(Marque, null=True, blank=True, on_delete=models.SET_NULL)
    categorie = models.ManyToManyField(Categorie)

    name = models.CharField("Nom du produit", max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text='Unique value for product page URL, created from name.')
    description = HTMLField("Description du produit", null=True, blank=True)
    image = models.ImageField("Ajouter une image", upload_to='produits/img/%Y/%m/%d', blank=True)

    prix = models.DecimalField("Prix de vente", max_digits=10, decimal_places=2)
    prix_reduit = models.DecimalField("Prix promo", max_digits=10, decimal_places=2, blank=True, null=True)

    disponible = models.BooleanField("Disponibilité", default=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, null=True, blank=True)
    is_bestseller = models.BooleanField(default=False)

    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag')

    creation = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField("Ajouté le", auto_now_add=False, default=datetime.datetime.now)

    def __str__(self):
        return "%s (%s)" % (self.name, ", ".join(categorie.name for categorie in self.categorie.all()),)

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review.all()))
        return np.mean(all_ratings)

    @property
    def view_product_count(self):
        return Produit.objects.filter(name=self).count()

    def get_absolute_url(self):
        return reverse('shop:detail_produit', args=[self.slug, self.id])

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Produit, self).save()

    class Meta:
        ordering = ['-name', '-creation']
        verbose_name = 'produit'
        verbose_name_plural = 'produits'
        index_together = (('id', 'slug'),)


class Review(models.Model):
    """docstring for Review"""
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    produit = models.ForeignKey(Produit, null=True, blank=True, related_name="review", on_delete=models.SET_NULL)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)


class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="cluster")

    def get_members(self):
        return "\n".join([u.username.user for u in self.users.all()])

    class Meta:
        verbose_name = "Cluster"
        verbose_name_plural = "Clusters"
