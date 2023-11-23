from django.urls import include, path
from rest_framework.routers import DefaultRouter

from django_store_assessment.stores.api.views import AddressViewSet, OpeningHoursViewSet, StoreViewSet

router = DefaultRouter()
router.register(r"stores", StoreViewSet)
router.register(r"addresses", AddressViewSet)
router.register(r"openinghours", OpeningHoursViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
