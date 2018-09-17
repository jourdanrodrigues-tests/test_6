from datetime import date

from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager
from django.utils.translation import ugettext as _


class CustomerQueryset(QuerySet):
    def that_should_be_billed(self) -> QuerySet:
        today = date.today()
        return self.filter(billing_day__gte=today.day, billing_day__lte=today.day + 2)


class CustomerManager(BaseManager.from_queryset(CustomerQueryset)):
    pass


class Customer(models.Model):
    billing_day = models.PositiveSmallIntegerField(_('billing day'))
    BILLING_DAY_ALLOWED_RANGE = range(1, 28)

    objects = CustomerManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.billing_day not in self.BILLING_DAY_ALLOWED_RANGE:
            raise Customer.BillingDayNotAllowed

        super().save(force_insert, force_update, using, update_fields)

    class BillingDayNotAllowed(Exception):
        pass
