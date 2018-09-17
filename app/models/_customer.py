from datetime import date

from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager
from django.utils.translation import ugettext as _

from app.models._models import User


class CustomerQueryset(QuerySet):
    def that_should_be_billed(self) -> QuerySet:
        today = date.today()
        return self.filter(
            billing_day__gte=today.day, billing_day__lte=today.day + 2,
        ).exclude(
            # Customers with bill events from this month or in the future shouldn't be billed
            bill_events__date__month__gte=today.month,
        )


class CustomerManager(BaseManager.from_queryset(CustomerQueryset)):
    pass


class Customer(models.Model):
    BILLING_DAY_ALLOWED_RANGE = range(1, 28)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    billing_day = models.PositiveSmallIntegerField(_('billing day'))

    objects = CustomerManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.billing_day not in self.BILLING_DAY_ALLOWED_RANGE:
            raise Customer.BillingDayNotAllowed

        super().save(force_insert, force_update, using, update_fields)

    class BillingDayNotAllowed(Exception):
        pass


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
