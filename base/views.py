from multiprocessing import context
from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q

# Create your views here.
# rooms = [
#     {'id': 1, 'name':'Lets learn python'},
#     {'id': 2, 'name':'Design with me'},
#     {'id': 3, 'name':'Frontend devops'},
# ]
def LoginPage(request):
    context={}
    return render(request,'base/login.html', context)     

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(host__username__icontains=q)
    )

    room_count = rooms.count()
    #querring upwards topic__name -> check models

    topics = Topic.objects.all()
    context = {'rooms': rooms,'topics':topics,'room_count':room_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    #get = select some FROM table X
    context = {'room': room}
    return render(request,'base/room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        #print(request.POST)
        form = RoomForm(request.POST)
        #знаем всё я форме
        if form.is_valid():
            form.save()
            #save() - return the model instance to the databse
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    #видно как было
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            #save() - return the model instance to the databse
            return redirect('home') 

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request,pk):
    room = Room.objects.filter(id=pk)
    if request.method == 'POST':
        room.delete()
        #save() - return the model instance to the databse
        return redirect('home') 
    
    return render(request,'base/delete.html', {'obj': room})
