# -*- coding: utf-8 -*-

"""
    ecommerce URL Configuration
"""

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

admin.autodiscover()

if 'rosetta' in settings.INSTALLED_APPS:
     urlpatterns = i18n_patterns(
          # path('__debug__/', include(debug_toolbar.urls)),
          path(_('admin/'), admin.site.urls),
          path(_('admin/doc/'), include('django.contrib.admindocs.urls')),
          path('', include('accounts.urls', namespace='accounts')),
          path(_('cart/'), include('panier.urls', namespace='panier')),
          path(_('orders/'), include('commandes.urls', namespace='commandes')),
          path(_('payment/'), include('payment.urls', namespace='payment')),
          path(_('coupons/'), include('coupons.urls', namespace='coupons')),
          path('rosetta/', include('rosetta.urls')),
          path('tinymce/', include('tinymce.urls')),
          path('', include('shop.urls', namespace='shop')),
    )

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
