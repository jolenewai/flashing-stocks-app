from django.shortcuts import render, redirect, reverse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.conf import settings
import stripe
from photos.models import Photo
from customers.models import Customer
from django.views.decorators.csrf import csrf_exempt

endpoint_secret = settings.SIGNING_SECRET

def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('shopping_cart', {})

    line_items = []

    for id, photo in cart.items():
        try:
            photo_object = Photo.objects.get(id=id)
        except ObjectDoesNotExist:
            photo_object = None
        
        line_items.append({
            'name': photo_object.caption,
            'amount': int(photo_object.price*100),
            'currency': 'usd',
            'quantity': 1
        })

    print(line_items)
    current_site = Site.objects.get_current()
    domain = current_site.domain

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        success_url=domain + reverse(checkout_success),
        cancel_url=domain + reverse(checkout_cancelled),
    )

    return render(request, 'checkout/checkout.template.html', {
        'session_id': session.id,
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })


def checkout_success(request):
    return HttpResponse('Checkout success')


def checkout_cancelled(request):
    return HttpResponse('Checkout cancelled')


@csrf_exempt
def payment_completed(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValuedError as e:
        #Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        #Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        handle_checkout_session(session)

    return HttpResponse(status=200)


def handle_checkout_session(session):
    print(session)



