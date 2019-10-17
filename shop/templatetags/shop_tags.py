from django import template
from ..models import Categorie, Produit, Review
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('shop/produit/shop_latest_produit.html')
def show_latest_products(count=10):
    latest_products = Produit.objects.filter(creation__isnull=False).order_by('-creation')[:count]
    context = { 'latest_products': latest_products }
    return context


# Review list views
@register.inclusion_tag('shop/produit/shop_review_list.html')
def show_review_list(count=10):
    latest_review_list = Review.objects.order_by('-pub_date', 'rating')[:count]
    context = {'latest_review_list':latest_review_list}
    return context
