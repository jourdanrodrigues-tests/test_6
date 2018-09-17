from rest_framework.filters import BaseFilterBackend


class CustomerUserFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(customer__user=request.user)
