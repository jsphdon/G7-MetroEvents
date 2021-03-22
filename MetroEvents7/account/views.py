from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .forms import CreateUserForm
from .models import User
from .decorators import unauthenticated_user


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='user')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            return redirect('account:login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            return redirect('account:myaccount')
        elif request.user.is_superuser:
            return redirect('account:administrator')
        else:
            return redirect('account:myaccount')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if not user.is_staff:
                    return redirect('account:myaccount')
                elif user.is_superuser:
                    return redirect('account:administrator')
                else:
                    return HttpResponse("ERROR")
            else:
                messages.info(request, 'Username OR password is incorrect')

        return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('account:login')


@login_required(login_url='login')
def adminPage(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'adminAccount.html', context)


# @login_required(login_url='login')
# def organizerPage(request):
#     if request.method == 'GET':
#         context = {}
#         return render(request, 'organizerAccount.html', context)

@login_required(login_url='login')
def homePage(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'useraccount.html', context)
