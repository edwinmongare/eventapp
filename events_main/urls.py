from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    checkoutView,
    OrderSummaryView,
    UserDashboard,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    add_single_item_to_cart,
    PaymentView,
    SearchView
)
from .models import Post
from django.contrib.auth.models import User
from . import views



#from users import views as user_views


urlpatterns = [
    
    #path('', PostListView.as_view(), name='events-home'),
	path('', PostListView.as_view(), name='events-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='users-profile'),
    path('order-summary', OrderSummaryView.as_view(), name='order-summary'),
    # path('Results/', search.as_view(), name='search'),
    path('Dashboard/', UserDashboard.as_view(), name='user-dashboard'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('searchresults/', SearchView.as_view(), name='Search-view'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('checkout/payment/<payment_options>/', PaymentView.as_view(), name='payment-view'),
    path('post/add_to_cart/<int:id>', views.add_to_cart, name= 'add-to-cart'),
    path('post/remove_from_cart/<int:id>', views.remove_from_cart, name= 'remove-from-cart'),
    path('post/remove_single_from_cart/<int:id>', views.remove_single_item_from_cart, name= 'remove_single_item_from_cart'),
    path('post/add_single_item_to_cart/<int:id>', views.add_single_item_to_cart, name= 'add_single_item_to_cart'),
    path('checkout/', checkoutView.as_view(), name='post-checkout'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/update/<int:pk>', PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post-delete'),
   	#path('', views.home, name='events-home'),
    #path('register/', user_views.register, name='register'),#
    path('about/', views.about, name='events-about'),
   

    

    


    path('profile/', views.profile, name='users-profile'),
    




]
