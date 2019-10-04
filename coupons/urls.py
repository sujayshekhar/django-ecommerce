from django.utils.translation import gettext_lazy as _
from django.urls import path
from . import views

app_name = 'coupons'
urlpatterns = [
    path(_('appliquer/'), views.utiliser_le_coupon, name='appliquer_le_coupon'),
]
