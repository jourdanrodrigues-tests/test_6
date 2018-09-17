from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.filters import CustomerUserFilter
from app.models import ChocolatePreference, Order
from app.serializers import ChocolatePreferenceSerializer, OrderSerializer


class ChocolatePreferenceViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = (IsAuthenticated,)
    filter_backends = (CustomerUserFilter,)
    serializer_class = ChocolatePreferenceSerializer
    queryset = ChocolatePreference.objects.all()

    def list(self, request):
        """
        This method makes this endpoint not 100% REST, but no API is 100% REST.
        """
        # Should have only one preference per customer
        queryset = self.filter_queryset(self.get_queryset()).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    filter_backends = (CustomerUserFilter,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
