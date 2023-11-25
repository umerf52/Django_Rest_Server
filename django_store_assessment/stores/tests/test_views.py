import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django_store_assessment.stores.models import Store
from django_store_assessment.stores.tests.factories import AddressFactory, OpeningHoursFactory, StoreFactory
from django_store_assessment.users.tests.factories import UserFactory

ALL_STORES_URL = reverse("store-list")


@pytest.fixture
def user():
    return UserFactory.create()


@pytest.fixture
def token(user):
    return Token.objects.create(user=user)


@pytest.fixture
def api_client(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


class TestStoreViewSet:
    @pytest.mark.django_db
    def test_create_store(self, api_client):
        payload = {
            "name": "Example Store",
            "address": {
                "street": "123 Example St",
                "city": "Example City",
                "state": "EX",
                "postal_code": "12345",
                "country": "Exampleland",
            },
            "opening_hours": [
                {"weekday": 1, "from_hour": "08:00", "to_hour": "17:00"},
                {"weekday": 2, "from_hour": "08:00", "to_hour": "17:00"},
            ],
        }

        response = api_client.post(ALL_STORES_URL, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Example Store"
        assert response.data["address"]["street"] == "123 Example St"
        assert response.data["address"]["city"] == "Example City"
        assert response.data["address"]["state"] == "EX"
        assert response.data["address"]["postal_code"] == "12345"
        assert response.data["address"]["country"] == "Exampleland"
        assert len(response.data["opening_hours"]) == 2
        assert response.data["opening_hours"][0]["weekday"] == 1
        assert response.data["opening_hours"][0]["from_hour"] == "08:00:00"
        assert response.data["opening_hours"][0]["to_hour"] == "17:00:00"
        assert response.data["opening_hours"][1]["weekday"] == 2
        assert response.data["opening_hours"][1]["from_hour"] == "08:00:00"
        assert response.data["opening_hours"][1]["to_hour"] == "17:00:00"

    @pytest.mark.django_db
    def test_create_store_without_address(self, api_client):
        payload = {
            "name": "Example Store",
            "opening_hours": [{"weekday": 1, "from_hour": "08:00", "to_hour": "17:00"}],
        }

        response = api_client.post(ALL_STORES_URL, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Example Store"
        assert not response.data["address"]
        assert len(response.data["opening_hours"]) == 1
        assert response.data["opening_hours"][0]["weekday"] == 1
        assert response.data["opening_hours"][0]["from_hour"] == "08:00:00"
        assert response.data["opening_hours"][0]["to_hour"] == "17:00:00"

    @pytest.mark.django_db
    def test_create_store_without_opening_hours(self, api_client):
        payload = {
            "name": "Example Store",
            "address": {
                "street": "123 Example St",
                "city": "Example City",
                "state": "EX",
                "postal_code": "12345",
                "country": "Exampleland",
            },
        }

        response = api_client.post(ALL_STORES_URL, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Example Store"
        assert response.data["address"]["street"] == "123 Example St"
        assert response.data["address"]["city"] == "Example City"
        assert response.data["address"]["state"] == "EX"
        assert response.data["address"]["postal_code"] == "12345"
        assert response.data["address"]["country"] == "Exampleland"
        assert not response.data["opening_hours"]

    @pytest.mark.django_db
    def test_create_store_without_address_and_opening_hours(self, api_client):
        payload = {
            "name": "Example Store",
        }

        response = api_client.post(ALL_STORES_URL, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Example Store"
        assert not response.data["address"]
        assert not response.data["opening_hours"]

    @pytest.mark.django_db
    def test_create_2_stores_with_same_opening_hours(self, api_client):
        opening_hours = {"weekday": 1, "from_hour": "08:00", "to_hour": "17:00"}
        payload1 = {
            "name": "Example Store 1",
            "opening_hours": [opening_hours],
        }
        response1 = api_client.post(ALL_STORES_URL, payload1, format="json")
        assert response1.status_code == status.HTTP_201_CREATED

        payload2 = {
            "name": "Example Store 2",
            "opening_hours": [opening_hours],
        }
        response2 = api_client.post(ALL_STORES_URL, payload2, format="json")
        assert response2.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_create_store_without_name_fails(self, api_client):
        payload = {
            "address": {
                "street": "123 Example St",
                "city": "Example City",
                "state": "EX",
                "postal_code": "12345",
                "country": "Exampleland",
            },
            "opening_hours": [{"weekday": 1, "from_hour": "08:00", "to_hour": "17:00"}],
        }

        response = api_client.post(ALL_STORES_URL, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_create_store_with_invalid_opening_hours_fails(self, api_client):
        payload = {
            "name": "Example Store",
            "address": {
                "street": "123 Example St",
                "city": "Example City",
                "state": "EX",
                "postal_code": "12345",
                "country": "Exampleland",
            },
            "opening_hours": [
                {"weekday": 1, "from_hour": "17:00", "to_hour": "08:00"}  # from_hour is greater than to_hour
            ],
        }

        response = api_client.post(ALL_STORES_URL, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_get_all_stores(self, api_client):
        StoreFactory.create_batch(2)

        response = api_client.get(ALL_STORES_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    @pytest.mark.django_db
    def test_get_store(self, api_client):
        store = StoreFactory.create()

        url = reverse("store-detail", args=[store.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == store.name
        assert response.data["address"]["street"] == store.address.street
        assert response.data["address"]["city"] == store.address.city
        assert response.data["address"]["state"] == store.address.state
        assert response.data["address"]["postal_code"] == store.address.postal_code
        assert response.data["address"]["country"] == store.address.country
        assert len(response.data["opening_hours"]) == 0

    @pytest.mark.django_db
    def test_get_non_existent_store(self, api_client):
        url = reverse("store-detail", args=[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_store(self, api_client):
        store = StoreFactory.create(name="Original Name", address=None)
        assert store.name == "Original Name"
        assert not store.address
        assert len(store.opening_hours.all()) == 0

        payload = {
            "name": "Updated Store",
            "address": {
                "street": "123 Updated St",
                "city": "Updated City",
                "state": "UP",
                "postal_code": "54321",
                "country": "Updatedland",
            },
            "opening_hours": [{"weekday": 1, "from_hour": "08:00", "to_hour": "17:00"}],
        }

        url = reverse("store-detail", args=[store.id])
        response = api_client.put(url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Store"
        assert response.data["address"]["street"] == "123 Updated St"
        assert response.data["address"]["city"] == "Updated City"
        assert response.data["address"]["state"] == "UP"
        assert response.data["address"]["postal_code"] == "54321"
        assert response.data["address"]["country"] == "Updatedland"
        assert len(response.data["opening_hours"]) == 1
        assert response.data["opening_hours"][0]["weekday"] == 1
        assert response.data["opening_hours"][0]["from_hour"] == "08:00:00"
        assert response.data["opening_hours"][0]["to_hour"] == "17:00:00"

    @pytest.mark.django_db
    def test_delete_store(self, api_client):
        store = StoreFactory.create()

        url = reverse("store-detail", args=[store.id])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Store.objects.filter(id=store.id).exists()

    @pytest.mark.django_db
    def test_delete_non_existent_store(self, api_client):
        url = reverse("store-detail", args=[1])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_get_without_proper_token(self):
        client = APIClient()
        response = client.get(ALL_STORES_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_get_with_invalid_token(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + "some_invalid_token")
        response = client.get(ALL_STORES_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_create_store_without_proper_token(self):
        client = APIClient()
        payload = {
            "name": "Example Store",
        }

        response = client.post(ALL_STORES_URL, payload, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_update_store_without_proper_token(self):
        client = APIClient()
        store = StoreFactory.create(name="Original Name", address=None)

        payload = {
            "name": "Updated Store",
        }

        url = reverse("store-detail", args=[store.id])
        response = client.put(url, payload, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_delete_store_without_proper_token(self):
        client = APIClient()
        store = StoreFactory.create()

        url = reverse("store-detail", args=[store.id])
        response = client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_filter_by_name(self, api_client):
        StoreFactory.create_batch(2)
        store = StoreFactory.create(name="Example Store")

        response = api_client.get(ALL_STORES_URL, {"name": "Example Store"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == store.name

    @pytest.mark.django_db
    def test_filter_by_address(self, api_client):
        StoreFactory.create_batch(2)
        address = AddressFactory.create(street="123 Example St")
        store = StoreFactory.create(
            address=address,
        )

        response = api_client.get(ALL_STORES_URL, {"address__street": "123 Example St"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == store.name

    @pytest.mark.django_db
    def test_filter_by_opening_hours(self, api_client):
        temp_stores = StoreFactory.create_batch(2)
        for ts in temp_stores:
            ts.opening_hours.add(OpeningHoursFactory.create(weekday=2))
        store = StoreFactory.create()
        opening_hours1 = OpeningHoursFactory.create(weekday=1)
        opening_hours2 = OpeningHoursFactory.create(weekday=2)
        store.opening_hours.add(opening_hours1.id, opening_hours2.id)

        response = api_client.get(ALL_STORES_URL, {"opening_hours__weekday": 1})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == store.name

    @pytest.mark.django_db
    def test_get_paginated_results(self, api_client):
        StoreFactory.create_batch(11)

        response = api_client.get(ALL_STORES_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 10
        assert response.data["count"] == 11
        assert response.data["next"] is not None
        assert response.data["previous"] is None

        # Get the next page
        response = api_client.get(response.data["next"])
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["count"] == 11
        assert response.data["next"] is None
        assert response.data["previous"] is not None
