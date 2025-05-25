from paypal.standard.models import ST_PP_COMPLETED
#// this tells us when the payment is completed

from paypal.standard.ipn.signals import valid_ipn_received
#// allow us to validate the IPN

from django.dispatch import receiver
#// allow us to receive the signal

from django.conf import settings
#// we want to pull out the "PAYPAL_RECEIVER_EMAIL = 'business@shamelesis.com'"

import time
#// do some timing stuff

import .models import Order


@receiver(valid_ipn_received)
def paypal_payment_receiver(sender, **kwargs):
    # add a 10 second pause for PayPal to send IPN data
    time.sleep(10)

    # grab the info that PayPal sends
    paypal_obj = sender
    # grab the invoice
    my_Invoice = str(paypal_obj.invoice)

    # match PayPal invoice to the order invoice
    # look up the order
    my_Order = Order.objects.get(invoice=my_Invoice)

    # Record the Order was paid
    my_Order.paid = True
    my_Order.save()