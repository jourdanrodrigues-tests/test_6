from django.db import transaction
from rest_framework import serializers

from app.models import ChocolatePreference, Order


class SaveWithCustomerMixin:
    """
    Works together with ModelSerializer
    """

    def save(self: serializers.ModelSerializer, **kwargs) -> None:
        super().save(customer=self.request.user.customer, **kwargs)


class ChocolatePreferenceSerializer(SaveWithCustomerMixin, serializers.ModelSerializer):
    class Meta:
        model = ChocolatePreference
        fields = ('dark', 'milk', 'white')


class OrderSerializer(SaveWithCustomerMixin, serializers.ModelSerializer):
    def _save_and_charge(self, **kwargs):
        with transaction.atomic():
            super().save(**kwargs)

            order = self.instance
            order.customer.charge(order.value)

    def save(self, **kwargs):
        if self.validated_data['closed']:
            self._save_and_charge(**kwargs)
        else:
            super().save(**kwargs)

    class Meta:
        model = Order
        fields = ('closed', 'chocolate_selection', 'value')
