from rest_framework import viewsets

from django_store_assessment.stores.api.serializers import AddressSerializer, OpeningHoursSerializer, StoreSerializer
from django_store_assessment.stores.models import Address, OpeningHours, Store

# Create your views here.


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class OpeningHoursViewSet(viewsets.ModelViewSet):
    queryset = OpeningHours.objects.all()
    serializer_class = OpeningHoursSerializer
