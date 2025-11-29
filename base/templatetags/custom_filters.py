from django import template

register = template.Library()

@register.filter
def category_color(category_id):
    try:
        if not category_id:
            return 1
        return (int(category_id) - 1) % 10 + 1
    except (ValueError, TypeError):
        return 1
