from email.message import EmailMessage
from io import BytesIO
import weasyprint
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from shop.setlang import strip_language
from django.utils.translation import gettext_lazy as _
from commandes.models import Commande
from ecommerce.settings import gateway


def payment_process(request):
    next_lang = strip_language(request.path)
    id_commande = request.session.get('id_commande')
    commande = get_object_or_404(Commande, id=id_commande)

    page_title_error = _('payement error')
    page_title_succes = _('payement succes')

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
            subject = "unsta Inc - Commande N°{}".format(commande.id)
            message = _('Please, find attached the invoice for your recent purchace.')
            email = EmailMessage(subject, message, 'admin@myshop.com', [commande.email])
            # genere un pdf
            html = render_to_string('commandes/commande/pdf.html', {'commande': commande})
            output = BytesIO()
            stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/admin.pdf')]
            weasyprint.HTML(string=html).write_pdf(output, stylesheets=stylesheets)
            # on attache le pdf au mail
            email.attach('commande_{}.pdf'.format(commande.id),
                         output.getvalue(), 'application/pdf')
            # On envoi le tout au mail
            email.send()

            return redirect('payment:valider')
        else:
            return redirect('payment:annuler')
    else:
        # On genere un token
        client_token = gateway.client_token.generate()

        context = { 'commande': commande, 'client_token': client_token,
            'page_title': page_title_succes, 'next': next_lang }
        template = 'payment/process.html'
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
