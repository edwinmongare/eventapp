from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as user_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm , LoginViewForm
from events_main.models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

import random
import socket
import uuid

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            # send_mail(
            #     'Account creation', 
            #  f'You have succesfuly registered an account with us, your username is{username}'
            # 'Testmail <edwinmongare14@gmail.com>', 
            # ['angelangugi75@gmail.com'],
            # fail_silently=False,
            # )

            send_mail(
                'Account creation',
                'Test sign up message, username angiengugi143',
                'Testmail <edwinmongare14@gmail.com',
                ['angiengugi75@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, f'Your account has been created! You can now succesfuly login')
            return redirect('login')
            

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
       #print("request.POST:" , request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        

        if user is not None:
            
            otp = random.randint(100000,1000000)
            s = SessionStore()
            s.create()
            the_id = s.session_key
            s['username'] = username
            s['password'] = password
            s['otp'] = otp 
            s.save()
           #print("s['otp']",  s['otp'] )
            message =f"Kindly use this code to login to your account {otp}"
            print("message", message)

            send_mail(
                'your one time login paswword', 
            message,
            'Testmail <edwinmongare14@gmail.com>', 
            [user.email]
            

                
                )
            
            # send_mail(

            #         ' your one time login paswword ',
            #         message, 
            #         'edwinmongare14@gmail.com',
            #         [user.email],
            #         fail_silently=False,
            #     )
               
            #Redirect to a success page.
            return HttpResponseRedirect(reverse('events-otp', args=(the_id,)))
                
        else:
            messages.success(request, f'Could not log you in')
            # Return an 'invalid login' error message.
    else:
        form = LoginViewForm()
    return render(request, 'users/login.html',  {'form': form})



def otp_login(request, url_id):
     if request.method == 'POST':
        s = SessionStore(session_key = url_id)
        existing_otp = s['otp']
        existing_username = s['username']
        existing_password = s['password']
        user_otp = request.POST['otp']
        user = authenticate(request, username=existing_username, password=existing_password)
        print("before if")
        print("existing_otp", existing_otp )
        print("user_otp", user_otp )
        if int(user_otp) ==  int(existing_otp):
            user_login(request, user)
            hostname = socket.gethostname()
            IP = socket.gethostbyname(hostname)
            message_login = f"Someone just logged into your account, \n device name  = {hostname} \n  ip address  = {IP}"

            send_mail(

                ' loggin activity ',
                message_login, 
                'Testmail <edwinmongare14@gmail.com>',
                [user.email],
                fail_silently=False,
            )

            return HttpResponseRedirect(reverse('events-home'))
        else:
            print("after else")
            messages.success(request, f'Could not log you in otp')
            return render(request, 'users/otp.html')
        messages.success(request, f'invalid otp code')

     else:
        return render(request, 'users/otp.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': Post.objects.all()
    }

    return render(request, 'users/profile.html', context)



class UserPostListView(ListView):
    model = Post
    template_name = 'users/profile.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

# #class UserDashboard(ListView):
#     model = Post
#     template_name = 'users/dashboard.html' 
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 6

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Post.objects.filter(author=user).order_by('-date_posted')