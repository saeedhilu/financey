from celery import shared_task
from .models import Transaction
from datetime import date

@shared_task
def process_recurring_transactions():
    print(f"Running recurring transactions on {date.today()}...")
    return "Done"

@shared_task
def send_emi_reminders():
    print("Checking EMI debts...")
    return "Reminders dispatched"
