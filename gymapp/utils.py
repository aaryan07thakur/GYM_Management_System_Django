
from datetime import datetime, date
from django.utils import timezone
from django.contrib import messages




def validate_date(request, date_str, field_name="Date"):
    """
    Converts string to date object and checks future date.
    Returns date object or None if invalid.
    """
    if not date_str or not isinstance(date_str, str):
        messages.error(request, f"{field_name} is required.")
        return None
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        messages.error(request, f"Invalid {field_name} format!")
        return None

    if date_obj > date.today():
        messages.error(request, f"Future {field_name} is not allowed!")
        return None

    return date_obj
