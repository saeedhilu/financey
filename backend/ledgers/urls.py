from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LedgerViewSet

router = DefaultRouter()
router.register('', LedgerViewSet, basename='ledger')

urlpatterns = [
    path('', include(router.urls)),
]
