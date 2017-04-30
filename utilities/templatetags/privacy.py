from django import template
from django.conf import settings

register = template.Library()


@register.assignment_tag
def get_privacy():
    return settings.PRIVACY

