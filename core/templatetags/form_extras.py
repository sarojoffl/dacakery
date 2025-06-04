from django import template

register = template.Library()

@register.filter
def get_field(form, field_name):
    try:
        return form[field_name]
    except Exception:
        return None
