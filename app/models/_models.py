from datetime import date

from django.db import models
from django.utils.translation import ugettext as _

from app.models._customer import Customer
from app.models._user import User


class SubscriptionValue(models.Model):
    value = models.FloatField(_('value'), editable=False)
    date = models.DateField(_('date'), auto_now=True, editable=False)
    user_responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions_added')


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
