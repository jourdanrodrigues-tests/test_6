from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models import ChocolatePreference
from app.serializers import ChocolatePreferenceSerializer


class ChocolatePreferenceViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChocolatePreferenceSerializer
    queryset = ChocolatePreference.objects.all()

    def get_queryset(self):
        return self.queryset.filter(customer__user=self.request.user)

    def list(self, request):
        """
        This method makes this endpoint not 100% REST, but no API is 100% REST.
        """
        # Should have only one preference per customer
        queryset = self.filter_queryset(self.get_queryset()).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
