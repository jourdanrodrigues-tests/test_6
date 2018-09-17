from datetime import date

import stripe
from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager
from django.utils.translation import ugettext as _

from app.models._user import User
from app.utils import Card


class CustomerQueryset(QuerySet):
    def that_should_receive_recommendations(self) -> QuerySet:
        today = date.today()
        return self.filter(billing_day=today.day + 2)

    def with_preferences_set_up(self):
        return self.filter(chocolate_preference__isnull=False)

    def that_should_be_billed(self) -> QuerySet:
        today = date.today()
        return self.filter(billing_day=today.day)


class CustomerManager(BaseManager.from_queryset(CustomerQueryset)):
    pass


class Customer(models.Model):
    BILLING_DAY_ALLOWED_RANGE = range(1, 28)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    billing_day = models.PositiveSmallIntegerField(_('billing day'))
    card_token = models.CharField(max_length=200)

    objects = CustomerManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.billing_day not in self.BILLING_DAY_ALLOWED_RANGE:
            raise Customer.BillingDayNotAllowed

        super().save(force_insert, force_update, using, update_fields)

    def generate_card_token(self, card: Card) -> str:
        # Creates the card/source via Stripe (couldn't figure how to do it)
        self.card_token = 'tok_mastercard'
        self.save(update_fields=['card_token'])
        return self.card_token

    def charge(self, value) -> None:
        if self.has_subscription():
            multiplier = self.subscription.get_multiplier()
            value *= multiplier

        stripe.Charge.create(  # Or something like this for charging
            amount=value,
            currency='usd',
            source=self.card_token,
            description='Charge for {}'.format(self.user.email),
        )

    def has_subscription(self) -> bool:
        return hasattr(self, 'subscription')  # OneToOneField

    class BillingDayNotAllowed(Exception):
        pass
