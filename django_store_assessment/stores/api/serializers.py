from rest_framework import serializers

from django_store_assessment.stores.models import Address, OpeningHours, Store


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["street", "city", "state", "postal_code", "country"]


class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = ["weekday", "from_hour", "to_hour"]


class StoreSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    opening_hours = OpeningHoursSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ["name", "address", "opening_hours"]
