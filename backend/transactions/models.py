from django.db import models
from django.conf import settings
from ledgers.models import Ledger

class Transaction(models.Model):
    class RecurrenceType(models.TextChoices):
        NONE = 'NONE', 'None'
        DAILY = 'DAILY', 'Daily'
        WEEKLY = 'WEEKLY', 'Weekly'
        MONTHLY = 'MONTHLY', 'Monthly'
        YEARLY = 'YEARLY', 'Yearly'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    # Double-entry system: value moves from credit to debit
    credit_ledger = models.ForeignKey(Ledger, on_delete=models.PROTECT, related_name='credit_transactions')
    debit_ledger = models.ForeignKey(Ledger, on_delete=models.PROTECT, related_name='debit_transactions')
    
    date = models.DateField()
    notes = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    payment_mode = models.CharField(max_length=50, blank=True)
    
    # Recurrence and EMI tracking
    is_recurring = models.BooleanField(default=False)
    recurrence_type = models.CharField(max_length=20, choices=RecurrenceType.choices, default=RecurrenceType.NONE)
    parent_transaction = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='recurring_instances')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.amount} from {self.credit_ledger} to {self.debit_ledger}"
