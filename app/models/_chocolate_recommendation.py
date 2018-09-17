from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Manager, QuerySet
from django.utils.translation import ugettext as _

from app.models._customer import Customer
from app.utils import SuperChocolateAPI


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

    def email_customer(self):
        """
        Sends email to customer, somehow.
        """
        pass
