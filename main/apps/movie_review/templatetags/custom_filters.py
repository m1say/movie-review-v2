from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter(name="biggest_timesince")
def biggest_timesince_filter(value, arg=None):
    """Format a date as the time since that date but only returns the first time unit."""
    ret = ""
    if not value:
        return ret
    try:
        if arg:
            ret = timesince(value, arg, depth=1)
        else:
            ret = timesince(value, depth=1)
    except (ValueError, TypeError):
        return ""
    return ret
