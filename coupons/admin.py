# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Coupon

# Register your models here.

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']

    class Meta:
        verbose_name = "CouponAdmin"
        verbose_name_plural = "CouponAdmins"

    def __str__(self):
        return self.list_display
