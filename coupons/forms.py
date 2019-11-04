# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _


class CouponForm(forms.Form):
    """docstring for CouponForm"""
    code = forms.CharField(
        label=_('Coupon'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-0 shadow-none',
                'placeholder': _('Apply coupon'),
                'aria-describedby': 'btnCoupon',
                'autocomplete': 'false'
            }))
