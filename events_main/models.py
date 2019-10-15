from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.conf import settings


CATEGORY_CHOICES = (
    ('Technology', 'Technology'), 
    ('Food', 'Food'), 
    ('Health', 'Health'),
    ('Meetups', 'Meetups'), 
    ('Cooking', 'Cooking')
)




class Post(models.Model):
    events = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='event_pictures')
    price = models.FloatField(null=True)
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)


    

    def __str__(self):
    	return self.events

    	
    def save(self):
        super().save()

        img = Image.open(self.image.path)


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'id': self.id})

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'id': self.id})




class OrderPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.post.events}"

    def get_total_post_price(self):
        return self.quantity * self.post.price

    def get_total_discount_post_price(self):
        return self.quantity * self.post.discount_price

    def get_amount_saved(self):
        return self.get_total_post_price() - self.get_total_discount_post_price()

    def get_final_price(self):
        if self.post.discount_price:
            return self.get_total_discount_post_price()
        return self.get_total_post_price()

  


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(OrderPost)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(default=timezone.now)
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username


    def get_total(self):
        total = 0
        for order_post in self.posts.all():
            total += order_post.get_final_price()
        return total

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
