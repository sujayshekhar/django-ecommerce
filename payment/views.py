from email.message import EmailMessage
from io import BytesIO
import weasyprint
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from shop.setlang import strip_language

from commandes.models import Commande
from ecommerce.settings import gateway


def payment_process(request):
    next_lang = strip_language(request.path)
    id_commande = request.session.get('id_commande')
    commande = get_object_or_404(Commande, id=id_commande)

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
            message = 'Please, find attached the invoice for your recent purchace.'
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
            
            return redirect('payment:valider', {'next': next_lang})
        else:
            return redirect('payment:annuler', {'next': next_lang})
    else:
        # On genere un token
        client_token = gateway.client_token.generate()
        return render(request,
                      'payment/process.html',
                      {'commande': commande,
                       'client_token': client_token,
                       'next': next_lang})


# Vue du paiement validé
def payment_done(request):
    next_lang = strip_language(request.path)
    return render(request, 'payment/payment_done.html', {'next': next_lang})


# Vue du paiment annulé
def payment_canceled(request):
    next_lang = strip_language(request.path)
    return render(request, 'payment/payment_cancel.html', {'next': next_lang})
