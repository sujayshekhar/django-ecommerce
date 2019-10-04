# -*- coding: utf-8 -*-
import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Commande, ItemCommande


# Administration des commandes

class ItemCommandeInline(admin.TabularInline):
    model = ItemCommande
    raw_id_fields = ['produit']


# Commande d'administration pour exportation au format csv
def export_to_csv(madmin, request, queryset):
    option = madmin.model.meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename={}.csv".format(option.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in option.get_fields() if not field.many_to_many
              and not field.one_to_many]
    # Ecriture d'information sur la premiere ligne
    writer.writerow([field.verbose_name for field in fields])
    # Ecriture de donnee sur la premiere ligne
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Exporter le document'


def detail_commande(obj):
    return mark_safe('<a href="{}">Voir les details</a>'.format(
        reverse('commandes:detail_commande_admin', args=[obj.id])))


def pdf_commande(obj):
    return mark_safe('<a href="{}">Imprimer</a>'.format(
        reverse('commandes:pdf_commande_admin', args=[obj.id])))


pdf_commande.short_description = 'Imprimer'


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    """
        Admin View for Commande
    """
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'adresse', 'telephone', 'ville', 'payer',
                    'creer', detail_commande, pdf_commande]
    list_filter = ['payer', 'creer', 'updated']
    inlines = [ItemCommandeInline]
    search_fields = ['payer', 'creer']
    actions = [export_to_csv]
