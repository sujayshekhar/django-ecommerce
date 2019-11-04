# -*- coding: utf-8 -*-
#

from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = 'payment'

urlpatterns = [
    path(_('process/'), views.payment_process, name='process'),
    path(_('done/'), views.payment_done, name='valider'),
    path(_('canceled/'), views.payment_canceled, name='annuler')
]
