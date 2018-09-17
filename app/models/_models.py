from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _


class User(AbstractUser):
    pass


class SubscriptionValue(models.Model):
    value = models.FloatField(_('value'), editable=False)
    date = models.DateField(_('date'), auto_now=True, editable=False)
    user_responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions_added')
