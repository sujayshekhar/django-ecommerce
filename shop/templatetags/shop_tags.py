from django import template
from ..models import Categorie, Produit
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('shop/produit/shop_latest_produit.html')
def show_latest_products(count=10):
    latest_products = Produit.objects.order_by('-creation')[:count]
    context = { 'latest_products': latest_products }
    return context
