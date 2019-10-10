# -*- coding: utf-8 -*-

"""
    ecommerce URL Configuration
"""
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.autodiscover()

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns = i18n_patterns(
        path('', include('accounts.urls', namespace='accounts')),
        path(_('cart/'), include('panier.urls', namespace='panier')),
        path(_('orders/'), include('commandes.urls', namespace='commandes')),
        path(_('payment/'), include('payment.urls', namespace='payment')),
        path(_('coupons/'), include('coupons.urls', namespace='coupons')),
        path('rosetta/', include('rosetta.urls')),
        path('', include('shop.urls', namespace='shop')),
        path(_('admin/doc/'), include('django.contrib.admindocs.urls')),
        path(_('admin/'), admin.site.urls),
        path('tinymce/', include('tinymce.urls')),
        path('admin/password_reset/', auth_views.PasswordResetView.as_view(),
             name='admin_password_reset', ),
        path('admin/password_reset/done/',
             auth_views.PasswordResetDoneView.as_view(),
             name='password_reset_done',
             ),
        path('reset/<uidb64>/<token>/',
             auth_views.PasswordResetConfirmView.as_view(),
             name='password_reset_confirm',
             ),
        path('reset/done/',
             auth_views.PasswordResetCompleteView.as_view(),
             name='password_reset_complete',
             ),
    )

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL,
          document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.COMPRESS_ROOT,
          document_root=settings.COMPRESS_ROOT)
     urlpatterns += static(settings.MEDIA_URL,
          document_root=settings.MEDIA_ROOT)
