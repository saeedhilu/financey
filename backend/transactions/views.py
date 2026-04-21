from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Transaction, EMIPlan
from .serializers import TransactionSerializer, EMIPlanSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EMIPlanViewSet(viewsets.ModelViewSet):
    serializer_class = EMIPlanSerializer
    def get_queryset(self):
        return EMIPlan.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        emi = self.get_object()
        if emi.months_paid >= emi.total_months:
            return Response({"detail": "EMI completed."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Process Double Entry Translation Automatically
        Transaction.objects.create(
            user=request.user,
            amount=emi.emi_amount,
            credit_ledger=emi.deduct_from_ledger,
            debit_ledger=emi.liability_ledger,
            date=timezone.now().date(),
            notes=f"EMI Payment: {emi.name} ({emi.months_paid + 1}/{emi.total_months})"
        )
        
        # Advance Timeline Iterator
        emi.months_paid += 1
        if emi.months_paid >= emi.total_months:
            emi.is_active = False
        emi.save()
        
        return Response(self.get_serializer(emi).data)
