from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Customer_page, Event
from django.contrib.auth.decorators import login_required
from .forms import EventForm, CustomerForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            profile = get_object_or_404(Profile, user=user)
            if profile.role == 'organizer':
                return redirect('organizer_page') 
            elif profile.role == 'customer':
                return redirect('customer_page') 
            else:
                return redirect('index') 
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role'] 
        
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)

                Profile.objects.create(user=user, role=role)

                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')
            except:
                messages.error(request, 'Username already exists or another error occurred.')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'register.html')




@login_required
def event_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.role != 'organizer':
        return redirect('index')  
    events = Event.objects.filter(instructor=profile)
    return render(request, 'event_list.html', {'events': events})

@login_required
def create_event(request):
    profile = get_object_or_404(User, id=request.user.id)  
    if profile.profile.role != 'organizer':  
        return redirect('index')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = profile
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})

@login_required
def update_event(request, event_id):
    profile = get_object_or_404(User, id=request.user.id)
    event = get_object_or_404(Event, id=event_id, organizer=profile)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'update_event.html', {'form': form})

@login_required
def delete_event(request, event_id):
    profile = get_object_or_404(User, id=request.user.id)
    event = get_object_or_404(Event, id=event_id, organizer=profile)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')

    return render(request, 'delete_event.html', {'event': event})


def event_list(request):
    events = Event.objects.all()  
    return render(request, 'event_list.html', {'events': events})

@login_required
def organizer_page(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.role != 'organizer':
        return redirect('index')  
    
    events = Event.objects.filter(organizer=profile.user)
    
    return render(request, 'organizer_page.html', {'events': events})

def customer_page(request):
    events = Event.objects.all()  
    return render(request, 'customer_page.html', {'events': events})

@login_required
def buy_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.quantity > 0:
        event.quantity -= 1  
        event.save()         
        messages.success(request, f'You successfully bought a ticket for {event.title}!')
    else:
        messages.error(request, f'Sorry, no tickets available for {event.title}.')

    return redirect('customer_page')  