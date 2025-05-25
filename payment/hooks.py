from paypal.standard.models import ST_PP_COMPLETED
#// this tells us when the payment is completed

from paypal.standard.ipn.signals import valid_ipn_received
#// allow us to validate the IPN

from django.dispatch import receiver
#// allow us to receive the signal

from django.conf import settings
#// we want to pull out the "PAYPAL_RECEIVER_EMAIL = 'business@shamelesis.com'"


@receiver(valid_ipn_received)
def paypal_payment_receiver(sender, **kwargs):

    # grab the info PayPal sends
    paypal_obj = sender
    print(paypal_obj)
    print(paypal_obj.mc_gross)
