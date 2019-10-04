# -*- coding: utf-8 -*-


from shop.setlang import strip_language
import weasyprint
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string

from .tasks import task_commande

from .models import ItemCommande, Commande
from .forms import FormCreationCommande
from panier.panier import Panier


# Create your views here.

@staff_member_required
def pdf_commande_admin(request, id_commande):
    commande = get_object_or_404(Commande, id=id_commande)
    html = render_to_string('commandes/commande/pdf.html',
        {'commande': commande})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="commande_{}.pdf"'.format(commande.id)
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/bootstrap.min.css')])
    return response


def creer_commande(request):
    next_lang = strip_language(request.path)
    panier = Panier(request)
    if request.method == 'POST':
        formulaire = FormCreationCommande(request.POST)
        if formulaire.is_valid():
            commande = formulaire.save(commit=False)
            if panier.coupon:
                commande.coupon = panier.coupon
                commande.discount = panier.coupon.discount
            commande.save()
            for item in panier:
                ItemCommande.objects.create(commande=commande,
                    produit=item['produit'],
                    prix=item['prix'], quantite=item['quantite'])
            # effacer les elements du panier
            panier.clear_session()
            # On demarre la tache
            task_commande.delay(commande.id)
            # on fixe l'ordre dans la session
            request.session['id_commande'] = commande.id
            # et redirige vers l'espace de paiment
            return redirect(reverse("payment:process"))
    else:
        formulaire = FormCreationCommande()
    return render(request, 'commandes/commande/create.html',
        {'panier': panier, 'formulaire': formulaire, 'next': next_lang })


@staff_member_required
def detail_commande_admin(request, id_commande):
    commande = get_object_or_404(Commande, id=id_commande)
    return render(request,
        'admin/commandes/commande/detail_commande.html',
        {'commande': commande})
