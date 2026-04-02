
from datetime import datetime, date
from django.utils import timezone
from django.contrib import messages



def validate_purchase_date(request, date_str):
    """
    Converts string to date object and checks future date.
    Returns (date_object or None)
    Adds message in case of error.
    """
    if not date_str:
        return timezone.now().date()
    try:
        purchase_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        messages.error(request, "Invalid date format!")
        return None

    if purchase_date > date.today():
        messages.error(request, "Future date is not allowed!")
        return None

    return purchase_date
