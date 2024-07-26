from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from accounts.models import SiteProfile
from django.contrib import messages, auth
from rest_framework.authtoken.models import Token
from accounts.forms import RegistrationForm, ProfileForm, LoginForm
from accounts.models import Profile
import requests


# Create your views here.

def register(request):
    print(request.GET)
    if request.method == "POST":
        print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print('FORM VALID')
            form.password = request.POST.get('password')
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            user_profile = Profile(user=user)
            user_profile.save()
            return redirect('login')

    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context=context)


def login(request):
    print('REQUEST', request.POST)
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('username'),
                                     password=form.cleaned_data.get('password'))

            print('hello')
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Logged In!!!")
                return redirect('home')
        else:
            messages.error(request, "Incorrect Login")
            return redirect('login')
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context=context)


def logout(request):
    # profile = SiteProfile.objects.all().first()
    # context = {'profile':profile}
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Logged Out!!!')
    return redirect('login')


def profile(request, user_id):
    print(request.user.id, 'USER ID')
    profile = SiteProfile.objects.all().first()
    user_profile = Profile.objects.get(user_id=user_id)
    context = {'user_profile': user_profile, 'profile':profile}
    return render(request, 'accounts/profile.html', context=context)



def home(request):
    return render(request, 'home.html')

def matches(request):
    return render(request, 'accounts/matches.html')
