from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Entry, Memory
from django.views.decorators.csrf import csrf_exempt
from .forms import MemoryForm

@login_required
def home(request):
    entries = Entry.objects.filter(user=request.user).order_by('-date_posted')
    return render(request, 'home.html', {'entries': entries})

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                return redirect('home')
            except:
                messages.error(request, "Username already exists")
        else:
            messages.error(request, "Password do not match")
    return render(request, "registration/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_entry(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Entry.objects.create(user=request.user, text=text)
            return redirect('home')
    return render(request, 'add_entry.html')

@login_required
def memories_view(request):
    memories = Memory.objects.filter(user=request.user).order_by('-date_added')
    return render(request, 'memories.html', {'memories': memories})

@login_required
def add_memory(request):
    if request.method == 'POST':
        form = MemoryForm(request.POST, request.FILES)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.user = request.user
            memory.latitude = form.cleaned_data.get('latitude')
            memory.longitude = form.cleaned_data.get('longitude')
            memory.save()
            return redirect('memories')
    else:
        form = MemoryForm()
    return render(request, 'add_memory.html', {'form': form})