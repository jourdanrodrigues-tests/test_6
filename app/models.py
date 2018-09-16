from django.contrib.auth.models import AbstractUser

from django.db import models
from django.utils.translation import ugettext as _


class User(AbstractUser):
    pass


class Customer(models.Model):
    billing_day = models.PositiveSmallIntegerField(_('billing day'))
    BILLING_DAY_ALLOWED_RANGE = range(1, 28)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.billing_day not in self.BILLING_DAY_ALLOWED_RANGE:
            raise Customer.BillingDayNotAllowed

        super().save(force_insert, force_update, using, update_fields)

    class BillingDayNotAllowed(Exception):
        pass
