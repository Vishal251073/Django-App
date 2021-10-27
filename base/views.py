from collections import namedtuple
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Message, Room,Topic
from django.contrib import messages
from .forms import RoomForm,UserForm
# Create your views here.

# rooms = [
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Lets learn JS!'},
#     {'id':3, 'name':'Frontend Developers'},

# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exsist!!')

        #Authentication of the user
        user = authenticate(request,username=username,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or Password does not exsist!!')

    context = {'page':page}
    return render(request,'base/login_register.html',context)


def logOutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) ## Overviw this piece from the documentation
            user.username = user.username.lower() ##Why
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An Error Occurred During Registration")
    return render(request,'base/login_register.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        ) #i makes it case sensitive

    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    #Basically This filter is added to filter the recent activity of the particular page to render
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}

    return render(request,'base/home.html',context) #Basically 'rooms' means how we want to access it and rooms is the array of items containing the matter


def room(request,pk):
    room = Room.objects.get(id=pk)
    #We cannot use messages keyword as alredy used to render falsh messages 
    room_messages = room.message_set.all().order_by('-created') #Basically it is saying give us all the messages specific to this particular room
    # We can write this line beacause they are connected via foreign key
    participants = room.participants.all()
    # Getting list of all Participants in the list
    if request.method=='POST':
        message = Message.objects.create(
            user= request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk = room.id)
        #Just Like save method updates something create method creates and save sit into database as well
    context = {'room':room,'room_messages':room_messages,'participants':participants} # Passing the context as a dictionary and in the room.html we can use it by calling 'room.'
    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form  = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name = topic_name) # Basically What it does is it creates the new topic room if it is not present
        #Or it will updates it if it is present already
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False) # Toget an instance of the room we do so
        #     room.host = request.user
        #     room.save()
        return redirect('home')
    context = {'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

#Like create Room method we will create Update Room method
@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk) #pk is primary Key This is the We want toupdate on the screen
    #basically After making that room we want to update it like in real time chat what we do is updating the form
    #For knowing whether we are updating the particular room with particular id Correctly we will be sending an instance of that particular 
    #which we received by its primary key to get it updated
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    #During updation of the room we should send the data to particular room only
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        return redirect('home')

    context = {'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        room.delete() # Here We are basically deleting the particular from the database
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})#We are basicall sending the particular room as object and will ask from user
    #whether he wants to delete or not


#Delete Message 
@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete() # Here We are basically deleting the particular from the database
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    return render(request,'base/update-user.html',{'form':form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})

def activityPage(request):
    room_messages = Message.objects.filter()
    return render(request,'base/activity.html',{'room_messages':room_messages})