from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

# Create your views here.

# rooms = [
#     {'id':1, 'name':'python is funn'},
#     {'id':2, 'name':'wanna play django wango'},
#     {'id':3, 'name':'i am using this'},
# ]

def loginPage(request):
    
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist') 

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')
        
    context = {'page':page}
    return render(request, 'baseapp/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured")


    context = {'form':form}
    return render(request, 'baseapp/login_register.html', context)



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains = q) |
        Q(description__icontains=q)
        )
    
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'baseapp/home.html', context) 

def room(request, pk):
    room = Room.objects.get(id=pk)
    roomMessages = room.message_set.all().order_by('-created')#give all message of particular room
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect ('room', pk = room.id)

    context = {'room':room, 'roomMessages':roomMessages, 'participants':participants}
    return render(request, 'baseapp/room.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() # we can get all children of specfic object from a model
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user':user, 'rooms':rooms, 'topics':topics, 'room_messages':room_messages}
    return render(request, 'baseapp/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )

        return redirect('home')

        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     #line above gives an insatnce of data before
        #     #saving it
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')
        
    context = {'form':form, 'topics':topics}
    return render(request, 'baseapp/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('you can not update this')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid:
        #     form.save()
        #     return redirect('home')
    
    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'baseapp/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('you can not update this')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = {'obj':room}
    return render(request, 'baseapp/delete_room.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('you can not update this')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    context = {'obj':message}
    return render(request, 'baseapp/delete_room.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
   
    context = {'form':form}
    return render(request, 'baseapp/update-user.html', context)


def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(
        Q(name__icontains=q) 
        )
    context = {'topics':topics}
    return render(request, 'baseapp/topics.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages':room_messages}
    return render(request, 'baseapp/activity.html', context)