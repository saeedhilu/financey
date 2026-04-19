from django.db import models
from django.conf import settings
from ledgers.models import Ledger

class SavingsGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='savings_goals')
    name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    # Linked to an asset ledger where the money is saved
    linked_ledger = models.ForeignKey(Ledger, on_delete=models.SET_NULL, null=True, blank=True, related_name='linked_goals')
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def current_amount(self):
        pass # To be calculated via serializers based on the linked_ledger's balance

    def __str__(self):
        return f"{self.name} - {self.target_amount}"
