from django.contrib.sitemaps import Sitemap
from .models import Categorie
from django.urls import reverse


def lastmod(self, obj):
	return obj.name


class CatSitemaps(Sitemap):
	changefreq = 'always'
	priority = 0.5
	i18n = True
	
	def items(self):
		return Categorie.objects.all()
