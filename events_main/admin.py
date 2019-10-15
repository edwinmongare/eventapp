from django.contrib import admin
from .models import Post, OrderPost, Order


admin.site.register(Post)
admin.site.register(OrderPost)
admin.site.register(Order)


