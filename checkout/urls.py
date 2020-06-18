from django.urls import path

from .views import checkout, checkout_success, checkout_cancelled, payment_completed

urlpatterns = [
    path('', checkout, name='checkout'),
    path('success/<session_id>', checkout_success, name='checkout_success'),
    path('cancelled', checkout_cancelled, name='checkout_cancelled'),
    path('payment_completed', payment_completed)
]