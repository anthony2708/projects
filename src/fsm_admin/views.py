from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


def index(req):
    return render(req, 'home.html')


def signup(req):
    return render(req, 'registration/signup.html')



def signin(req):
    return render(req, 'registration/signin.html')


def register(req):
    if req.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if req.method == 'POST':
            form = CreateUserForm(req.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')

    context = {'form': form}
    return render(req, 'accounts/register.html', context)


def login(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            redirect('')

        else:
            messages.error(req, 'Username or Password is incorrect')

    context = {}
    return render(req, 'accounts/login.html', context)


def logoutUser(req):
    logout(req)
    return redirect('login')


