from django.urls import include, path
from rest_framework.routers import DefaultRouter

from django_store_assessment.stores.api.views import StoreViewSet

router = DefaultRouter()
router.register(r"stores", StoreViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
