import pytest

from django_store_assessment.stores.models import Address, OpeningHours, Store
from django_store_assessment.stores.tests.factories import AddressFactory, OpeningHoursFactory, StoreFactory


@pytest.mark.django_db
def test_address_factory():
    # Create an instance using the factory
    address = AddressFactory()

    # Assertions to ensure the factory is creating instances correctly
    assert isinstance(address, Address)
    assert address.street
    assert address.city
    assert address.state
    assert address.postal_code
    assert address.country


@pytest.mark.django_db
def test_opening_hours_factory():
    # Create an instance using the factory
    opening_hours = OpeningHoursFactory()

    # Assertions to ensure the factory is creating instances correctly
    assert isinstance(opening_hours, OpeningHours)
    assert opening_hours.weekday
    assert opening_hours.from_hour
    assert opening_hours.to_hour
    assert opening_hours.from_hour < opening_hours.to_hour


@pytest.mark.django_db
def test_store_factory():
    # Create an instance using the factory
    store = StoreFactory()

    # Assertions to ensure the factory is creating instances correctly
    assert isinstance(store, Store)
    assert store.name
    assert store.address
    assert store.opening_hours
