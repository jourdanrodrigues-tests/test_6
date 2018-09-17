from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _

from app.models._customer import Customer


class User(AbstractUser):
    pass


class CustomerBillEvent(models.Model):
    date = models.DateField(_('date'), default=date.today, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bill_events')
