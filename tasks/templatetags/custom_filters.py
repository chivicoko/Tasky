from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def format_due_date(value):
    # Check if the input is a datetime object or a string
    if isinstance(value, datetime):
        due_date = value
    elif isinstance(value, str):
        try:
            due_date = datetime.fromisoformat(value)
        except ValueError:
            return value
    else:
        return value

    current_date = datetime.now()

    if due_date.date() == current_date.date():
        return due_date.strftime('%I:%M %p')

    tomorrow = current_date + timedelta(days=1)
    if due_date.date() == tomorrow.date():
        return 'Tomorrow'

    formatted_date = due_date.strftime('%d/%m/%y')
    return formatted_date
