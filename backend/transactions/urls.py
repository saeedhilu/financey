from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, EMIPlanViewSet

router = DefaultRouter()
router.register('entries', TransactionViewSet, basename='transaction')
router.register('emi-plans', EMIPlanViewSet, basename='emiplan')

urlpatterns = [
    path('', include(router.urls)),
]
