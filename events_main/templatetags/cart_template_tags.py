from django import template
from events_main.models import Order

register = template.Library()


@register.filter
def cart_post_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].posts.count()
    return 0