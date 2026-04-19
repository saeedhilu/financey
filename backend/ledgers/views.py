from rest_framework import viewsets
from .models import Ledger
from .serializers import LedgerSerializer

class LedgerViewSet(viewsets.ModelViewSet):
    serializer_class = LedgerSerializer
    
    def get_queryset(self):
        return Ledger.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
