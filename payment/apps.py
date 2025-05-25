from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'

    # set up paypal IPN signal, so everytime this app runs, the following will
    # run in the background.
    def ready(self):
        import payment.hooks

