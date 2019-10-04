from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponForm


@require_POST
def utiliser_le_coupon(request):
    date_du_jour = timezone.now()
    formulaire = CouponForm(request.POST, auto_id='id_%s')
    if formulaire.is_valid():
        code = formulaire.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, valid_from__lte=date_du_jour,
                valid_to__gte=date_du_jour, active=True)
            request.session['id_coupon'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['id_coupon'] = None
    return redirect('panier:detail_panier')
