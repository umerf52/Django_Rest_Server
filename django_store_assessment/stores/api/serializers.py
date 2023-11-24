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
    address = AddressSerializer(required=False)
    opening_hours = OpeningHoursSerializer(many=True, required=False)

    def create(self, validated_data):
        address_data = validated_data.pop("address", None)
        address = None
        if address_data:
            address = Address.objects.create(**address_data)

        # Handle optional opening_hours
        opening_hours_data = validated_data.pop("opening_hours", [])
        store = Store.objects.create(address=address, **validated_data)

        for oh_data in opening_hours_data:
            opening_hour, created = OpeningHours.objects.get_or_create(**oh_data)
            store.opening_hours.add(opening_hour)

        return store

    def update(self, instance, validated_data):
        # Handle address update or creation
        address_data = validated_data.pop("address", None)
        if address_data:
            if instance.address:
                # Update existing address
                Address.objects.filter(id=instance.address.id).update(**address_data)
                instance.address.refresh_from_db()  # Refresh the instance's address
            else:
                # Create new address and associate with store
                address = Address.objects.create(**address_data)
                instance.address = address

        # Handle opening_hours update
        opening_hours_data = validated_data.pop("opening_hours", [])
        instance.opening_hours.clear()
        for oh_data in opening_hours_data:
            oh_obj, created = OpeningHours.objects.get_or_create(**oh_data)
            instance.opening_hours.add(oh_obj)

        # Update other fields of the Store instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    class Meta:
        model = Store
        fields = ["name", "address", "opening_hours"]
