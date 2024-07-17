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
    profile = SiteProfile.objects.all().first()
    print(request.GET)
    if request.method == "POST":
        print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
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

    context = {'profile': profile, 'form': form}
    return render(request, 'accounts/register.html', context=context)


def login(request):
    profile = SiteProfile.objects.all().first()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('username'),
                                     password=form.cleaned_data.get('password'))

            print('hello')
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Logged In!!!")
                return redirect('reg_index')
        else:
            messages.error(request, "Incorrect Login")
            return redirect('login')
    form = AuthenticationForm()
    context = {'profile': profile, 'form': form}
    return render(request, 'accounts/login.html', context=context)


def logout(request):
    # profile = SiteProfile.objects.all().first()
    # context = {'profile':profile}
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Logged Out!!!')
    return redirect('login')


def profile(request, user_id):
    profile = SiteProfile.objects.all().first()
    user_profile = Profile.objects.get(user_id=user_id)
    context = {'user_profile': user_profile, 'profile':profile}
    return render(request, 'accounts/profile.html', context=context)


def generate_api_key(request):
    if request.method == 'POST':
        url = 'http://localhost:8000/auth/jwt/create/'
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            data = requests.post(url, data={
                'username': user.username,
                'password': password,
            })
            response = data.json()
            api_key = response.get('access', 'NOT FOUND')
            user_profile = Profile.objects.get(user_id=request.user.id)
            user_profile.api_token = api_key
            user_profile.save()
            print(api_key)
            messages.success(request, 'API KEY GENERATED!!!')
        else:
            messages.error(request, 'Incorrect Password!!!')
    return redirect('profile', request.user.id)
