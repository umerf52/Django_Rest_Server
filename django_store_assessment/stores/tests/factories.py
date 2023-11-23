import datetime

import factory
from faker import Faker

from django_store_assessment.stores.models import Address, OpeningHours, Store

faker = Faker()


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    street = factory.LazyAttribute(lambda x: faker.street_address())
    city = factory.LazyAttribute(lambda x: faker.city())
    state = factory.LazyAttribute(lambda x: faker.state())
    postal_code = factory.LazyAttribute(lambda x: faker.postcode())
    country = factory.LazyAttribute(lambda x: faker.country())


class OpeningHoursFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OpeningHours

    weekday = factory.LazyAttribute(lambda x: faker.random_int(min=1, max=7))
    from_hour = datetime.time(9, 0)
    to_hour = datetime.time(20, 0)


class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Store

    name = factory.LazyAttribute(lambda x: faker.name())
    address = factory.SubFactory(AddressFactory)
