from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from django_store_assessment.stores.api.serializers import AddressSerializer, OpeningHoursSerializer, StoreSerializer
from django_store_assessment.stores.models import Address, OpeningHours, Store

# Create your views here.


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        "name",
        "address__street",
        "address__city",
        "address__state",
        "address__postal_code",
        "address__country",
        "opening_hours__weekday",
        "opening_hours__from_hour",
        "opening_hours__to_hour",
    ]
    search_fields = filterset_fields


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class OpeningHoursViewSet(viewsets.ModelViewSet):
    queryset = OpeningHours.objects.all()
    serializer_class = OpeningHoursSerializer
