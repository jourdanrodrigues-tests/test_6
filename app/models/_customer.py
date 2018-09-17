from datetime import date, datetime

import stripe
from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager, Manager
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField

from app.models._models import User
from app.utils import Card, SuperChocolateAPI


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


class ChocolateRecommendationManager(Manager):
    def generate_from_customer(self, customer: Customer) -> QuerySet:
        preference = customer.chocolate_preference
        recommendation = SuperChocolateAPI().get_recommendation(
            dark_ratio=preference.dark,
            milk_ratio=preference.milk,
            white_ratio=preference.white,
        )
        return self.create(customer=customer, recommendation=recommendation)


class ChocolateRecommendation(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='chocolate_recommendations',
        editable=False,
    )
    recommendation = JSONField(_('recommendation'), editable=False)
    date = models.DateTimeField(_('date'), default=datetime.now, editable=False)

    objects = ChocolateRecommendationManager()


class ChocolatePreference(models.Model):
    CHOICES = (
        (1, 'Hate'),
        (2, 'Dislike'),
        (3, 'Neutral'),
        (4, 'Like'),
        (5, 'Love'),
    )
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='chocolate_preference')
    milk = models.PositiveSmallIntegerField(_('milk'), choices=CHOICES)
    dark = models.PositiveSmallIntegerField(_('dark'), choices=CHOICES)
    white = models.PositiveSmallIntegerField(_('white'), choices=CHOICES)


class Subscription(models.Model):
    MONTHLY = 1
    SIX_MONTHS = 2
    LENGTH_CHOICES = (
        (MONTHLY, _('Monthly')),
        (SIX_MONTHS, _('6 months')),
    )

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    length = models.PositiveSmallIntegerField(choices=LENGTH_CHOICES)

    def get_multiplier(self) -> int:
        if self.length is Subscription.MONTHLY:
            return 1
        elif self.length is Subscription.SIX_MONTHS:
            return 6
        else:
            raise Subscription.InvalidLengthChoice

    class InvalidLengthChoice(Exception):
        pass


class CustomerBillEvent(models.Model):
    date = models.DateField(_('date'), default=date.today, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bill_events')


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    closed = models.BooleanField(_('closed'), default=False)
    # This is a simplification of what would be the order model
    chocolate_selection = models.CharField(_('chocolate selection'), max_length=200)
