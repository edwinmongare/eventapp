from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.utils import timezone
from .models import Post, Order, OrderPost, Payment
from users.forms import UserUpdateForm
import users 
from .forms import CheckoutForm


import stripe
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"



def home(request):
    
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'events_main/home.html', context)


def eventdetails(request):
    
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'events_main/eventdetails.html', context)


# class search(View):
#     def get(self, *args, **kwargs):
#          form = SeachForm()
#          context = {
#              'form': form,
#          }

#          return render(self.request,'events_main/base.html', context)
     

#     def post(self, *args, **kwargs):
#          form = SeachForm(self.request.POST or None)
#          search = Post.objects.get(events)


class checkoutView(View):
    def get(self, *args, **kwargs):
         form = CheckoutForm()
         context = {
             'form': form,
         }
    
    
         return render(self.request,'events_main/checkout.html', context)

    def post(self, *args, **kwargs):
         form = CheckoutForm(self.request.POST or None)
         try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                First_name = form.cleaned_data.get('First_name')
                Second_name = form.cleaned_data.get('Second_name')
                email_address = form.cleaned_data.get('email_address')
                phone_number = form.cleaned_data.get('phone_number')
                payment_option = form.cleaned_data.get('payment_option')
                order.save()

                print("data", form.cleaned_data)

                if payment_option == 'S':
                    return redirect("payment/Stripe/")
                else:
                    return redirect("payment/PayPal/")
                # return HttpResponseRedirect(reverse('post-checkout',))

                return render(self.request, 'events_main/order_summary.html',context)
         except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("events_main/order_summary.html")  

         

class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "events_main/payment.html")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token,
            # description="Charge for jenny.rosen@example.com"
        )

        # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

        
            order.ordered = True
            order.payment = payment
            order.save()
            messages.success(self.request, "Your order was successful!")
            return redirect("/")


        except stripe.error.CardError as e:
          # Since it's a decline, stripe.error.CardError will be caught
          body = e.json_body
          err  = body.get('error', {})

          messages.warning(self.request, f"{err.get('message')}")
          return redirect("/")
        except stripe.error.RateLimitError as e:
          # Too many requests made to the API too quickly
          messages.warning(self.request, "Rate limit error")
          return redirect("/")
          
        except stripe.error.InvalidRequestError as e:
          # Invalid parameters were supplied to Stripe's API
          messages.warning(self.request, "Invalid parameters" )
          return redirect("/")
         
        except stripe.error.AuthenticationError as e:
          # Authentication with Stripe's API failed
          # (maybe you changed API keys recently)
          messages.warning(self.request,"Not authenticated" )
          return redirect("/")
          
        except stripe.error.APIConnectionError as e:
          # Network communication with Stripe failed
          messages.warning(self.request, "Network error" )
          return redirect("/")
          
        except stripe.error.StripeError as e:
          # Display a very generic error to the user, and maybe send
          # yourself an email
          messages.warning(self.request,"Something went wrong. You were not charged. Please try again.")
          return redirect("/")
          
        except Exception as e:
          # Something else happened, completely unrelated to Stripe
          messages.warning(self.request,"A serious error occurred. We have been notifed." )
          return redirect("/")
          

class PostListView(ListView):
    model = Post
    template_name = 'events_main/home.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

class UserPostListView(ListView):
    model = Post
    template_name = 'events_main/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

# class SearchView(ListView):
#     model = Post
#     template_name = 'events_main/user_posts2.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     paginate_by = 6


#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Post.objects.filter(author=user).order_by('events')



class UserDashboard(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'users/dashboard.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6
    



class OrderSummaryView(DetailView):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(user=self.request.user, ordered=False)
            
            context = {
                'objects': order
            }
            return render(self.request, 'events_main/order_summary.html',context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class SearchView(DetailView):
    def get(self, *args, **kwargs):
        try:
            # post = Post.objects.filter(self.events)
            post = get_object_or_404(Post, events)
            post, created = Post.objects.get_or_create(
            events=events,
          
            )
            
            context = {
                'post': post
            }
            return render(self.request, 'events_main/user_posts2.html',context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "No results found")
            return redirect("/")
    

    

class PostDetailView(DetailView):
    model = Post
    template_name = 'events_main/post_detail.html'
    


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
    'events', 
    'content', 
    'image',
    'category',
    'price',  
    'discount_price']
    


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['events',
     'content', 
     'image', 
     'category', 
     'price' 
     'discount_price']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




def about(request):
    return render(request, 'events_main/about.html', {'events': 'About'})



def profile(request):
    context = {
    'u_form': u_form,
    'p_form': p_form,
    'posts': Post.objects.all()
    }

 
    return render(request, 'users/profile.html', context)

@login_required
def add_to_cart(request, id):
    post = get_object_or_404(Post, id=id)
    order_post, created = OrderPost.objects.get_or_create(
        post=post,
        user=request.user,
        ordered=False
        )
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.posts.filter(post__id=post.id).exists():
            print(post.id)
            order_post.quantity += 1
            order_post.save()
            messages.info(request, "This item quantity was updated.")
            return HttpResponseRedirect(reverse('post-detail', args=(id,)))
        else:
            order.posts.add(order_post)
            messages.info(request, "This item was added to your cart.")
            return HttpResponseRedirect(reverse('post-detail', args=(id,)))
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.posts.add(order_post)
        messages.info(request, "This item was added to your cart.")
        return HttpResponseRedirect(reverse('post-detail', args=(id,)))

# def searchresult(request, events):
#     post = get_object_or_404(Post, events = events)
#     result = Post.objects.filter(
#         events
#         )

def add_single_item_to_cart(request, id):
    post = get_object_or_404(Post, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.posts.filter(post__id=post.id).exists():

            order_post = OrderPost.objects.filter(

                post=post,
                user=request.user,
                ordered=False
            )[0]
            if order_post.quantity >= 1:
                order_post.quantity += 1
                order_post.save()
            else:
                order.posts.remove(order_post)
            messages.info(request, "This item quantity was updated.")
            return HttpResponseRedirect(reverse('order-summary'))
        else:
            messages.info(request, "This item was not in your cart.")
            return HttpResponseRedirect(reverse('post-detail', args=(id,)))
    else:
        messages.info(request, "You do not have an active order")
        return HttpResponseRedirect(reverse('post-detail', args=(id,)))



    #return HttpResponseRedirect(reverse('post-detail', args=(id,)))

     
        



def remove_from_cart(request, id):
    post = get_object_or_404(Post, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.posts.filter(post__id=post.id).exists():
            order_post = OrderPost.objects.filter(
                post=post,
                user=request.user,
                ordered=False
            )[0]
            order.posts.remove(order_post)
            messages.info(request, "This item was removed from your cart.")
            return HttpResponseRedirect(reverse('order-summary'))
        else:
            messages.info(request, "This item was not in your cart.")
            return HttpResponseRedirect(reverse('post-detail', args=(id,)))
    else:
        messages.info(request, "You do not have an active order")
        return HttpResponseRedirect(reverse('post-detail', args=(id,)))


def remove_single_item_from_cart(request, id):
    post = get_object_or_404(Post, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.posts.filter(post__id=post.id).exists():

            order_post = OrderPost.objects.filter(

                post=post,
                user=request.user,
                ordered=False
            )[0]
            if order_post.quantity > 1:
                order_post.quantity -= 1
                order_post.save()
            else:
                order.posts.remove(order_post)
            messages.info(request, "This item quantity was updated.")
            return HttpResponseRedirect(reverse('order-summary'))
        else:
            messages.info(request, "This item was not in your cart.")
            return HttpResponseRedirect(reverse('post-detail', args=(id,)))
    else:
        messages.info(request, "You do not have an active order")
        return HttpResponseRedirect(reverse('post-detail', args=(id,)))



    #return HttpResponseRedirect(reverse('post-detail', args=(id,)))

     
        