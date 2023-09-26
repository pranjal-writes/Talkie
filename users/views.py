from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponse
import re
from chat.models import Profile


# Create your views here.


def register(request):
    
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if get_user_model().objects.filter(username=uname).exists():
            messages.error(request, 'Please choose a unique username')
            return redirect('register')

        elif pass1 != pass2:
            messages.error(request, 'The passwords do not match')
            return redirect('register')
        elif not re.match(r'^[A-Za-z0-9_]+$', uname):
            messages.error(request, 'A username can only contain alphabets, numbers and underscores')
            return redirect('register')
        else:

            new_user = User.objects.create_user(username=uname,email=None, password=pass1)
            
            
            new_user.save()
            profile = Profile(user=new_user)
            profile.save()
            messages.success(
                request, 'Your account has been created successfully')
            return redirect('login')

    return render(request, 'users/signup.html')


def usercheck(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse('<div style="color:#ff1c3a; margin-top:6px;"> This username already exists.</div>')
    elif not re.match(r'^[A-Za-z0-9_]+$', username):
        return HttpResponse('<div style="color:#ff1c3a; margin-top:6px;"> A username can only contain alphabets, numbers and underscores.</div>')
    else:
        return HttpResponse('<div style="color:#04ff00; margin-top:6px;"> This username is available.</div>')


def login(request):
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('pass')
        user= authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Please enter valid username and password')
        

    return render(request, 'users/login.html')


def logout(request):
    auth_logout(request)
    return redirect('login')