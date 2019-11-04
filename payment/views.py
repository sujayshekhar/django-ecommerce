# -*- coding: utf-8 -*-
#


import weasyprint
from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect, render

from commandes.models import Commande
from ecommerce.settings import gateway
from shop.setlang import strip_language



def payment_process(request):
    next_lang = strip_language(request.path)
    id_commande = request.session.get('id_commande')
    commande = get_object_or_404(Commande, id=id_commande)

    page_title_error = _('payement error')
    page_title_succes = _('payement')

    if request.method == 'POST':
        # recuperation de la variable nonce : nombre arbitraire en cryptographie
        nonce = request.POST.get('payment_method_nonce', None)

        # On créer et on soumet la transaction
        result = gateway.transaction.sale({
            'amount': '{:.2f}'.format(commande.get_depense_total()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            # Si le resultat est valide, on marque
            # la commande comme payée
            commande.payer = True
            # On stocke l'identifiant unique de la transaction
            commande.id_braintree = result.transaction.id
            commande.save()
            # envoi de mail apres paiement
            subject = "e-market - commande N°{}".format(commande.id)
            message = 'Bonjour "{}\n\n", Merci de votre commande sur notre Boutique en ligne e-market.\n Nous\
            avons le plaisir de confirmer que nous l\'avons prise en compte et qu\'elle est déjà prête à\
            être expédiée.\n Nous vous adressons ci-dessous un récapitulatif ainsi que le numéro de\
            commande et le numéro de suivi de votre colis.\n\n\n Toute l\'équipe des Conseilliers et Conseillières\
            e-market est là pour vous accompagner : contactez-nous par téléphone au +225 00 000 000 du Lundi au Vendredi\
            entre 08 heures et 19 heures et le Samedi entre 09 heures et 18 heures. Vous pouvez\
            aussi nous adressez un e-mail : admin@emarket.com et nous vous répondons très vite.\n\n\n\
            Merci pour votre fidélité et à très vite sur votre Boutique en ligne e-market.\n\
            L\'équipe e-market.'.formart(commande.first_name)
            email = EmailMessage(subject, message, 'flavienhgs@gmail.com', [commande.email])
            # genere un pdf
            html = render_to_string('commandes/commande/pdf.html', {'commande': commande})
            output = BytesIO()
            stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/admin.pdf')]
            weasyprint.HTML(string=html).write_pdf(output, stylesheets=stylesheets)
            # on attache le pdf au mail
            email.attach('commande_{}.pdf'.format(commande.id), output.getvalue(), 'application/pdf')
            # On envoi le tout au mail
            email.send()

            return redirect('payment:valider')
        else:
            return redirect('payment:annuler')
    else:
        # generation de token
        client_token = gateway.client_token.generate()

        context = { 'commande': commande, 'client_token': client_token,
            'page_title': page_title_succes, 'next': next_lang }
        template = 'payment/payement_process.html'
        return render(request, template, context)


# Vue du paiement validé
def payment_done(request):
    next_lang = strip_language(request.path)
    page_title_succes = _('payement succes')
    context = {'next': next_lang, 'page_title': page_title_succes}
    template = 'payment/payment_done.html'

    return render(request, template, context)


# Vue du paiment annulé
def payment_canceled(request):
    next_lang = strip_language(request.path)
    page_title_error = _('payement error')
    context = {'next': next_lang, 'page_title': page_title_error}
    template = 'payment/payment_cancel.html'

    return render(request, template, context)
