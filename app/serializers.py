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
    class Meta:
        model = Order
        fields = ('customer', 'closed', 'chocolate_selection')
