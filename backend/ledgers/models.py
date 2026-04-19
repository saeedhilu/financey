from django.db import models
from django.conf import settings

class LedgerClass(models.TextChoices):
    ASSET = 'ASSET', 'Asset'
    LIABILITY = 'LIABILITY', 'Liability'
    INCOME = 'INCOME', 'Income'
    EXPENSE = 'EXPENSE', 'Expense'

class Ledger(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ledgers')
    name = models.CharField(max_length=255)
    ledger_class = models.CharField(max_length=50, choices=LedgerClass.choices)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_ledgers')
    is_system = models.BooleanField(default=False, help_text="System ledgers cannot be deleted")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'name', 'parent')

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
