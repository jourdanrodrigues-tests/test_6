from rest_framework import serializers

from app.models import ChocolatePreference


class ChocolatePreferenceSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        super().save(customer=self.request.user.customer, **kwargs)

    class Meta:
        model = ChocolatePreference
        fields = ('dark', 'milk', 'white')
