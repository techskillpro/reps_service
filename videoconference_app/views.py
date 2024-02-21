from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        try:
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'login.html', {'success': "Registration successful. Please login."})
            else:
                error_message = form.errors.as_text()
                return render(request, 'register.html', {'error': error_message})
        except:
            return HttpResponse('Error Encountered. COntact Admin For Help.')
    return render(request, 'register.html')


def login_view(request):
    if request.method=="POST":
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/conference/dashboard")
            else:
                return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})
        except:
            return HttpResponse('Error Encountered. COntact Admin For Help.')
    return render(request, 'login.html')

@login_required(login_url='user_login')
def dashboard(request):
    return render(request, 'dashboard.html', {'name': request.user.first_name})

@login_required(login_url='user_login')
def videocall(request):
    return render(request, 'videocall.html', {'name': request.user.first_name + " " + request.user.last_name})

@login_required(login_url='user_login')
def logout_view(request):
    try:
        logout(request)
        return redirect('base')
    except:
        return HttpResponse('Error Encountered. COntact Admin For Help.')

@login_required(login_url='user_login')
def join_room(request):
    if request.method == 'POST':
        try:
            roomID = request.POST['roomID']
            return redirect("/conference/meeting?roomID=" + roomID)
        except:
            return HttpResponse('Error Encountered. COntact Admin For Help.')        
    return render(request, 'joinroom.html')
