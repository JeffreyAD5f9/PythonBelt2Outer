from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import *

def userInit(request):
    if 'userCurrent' in request.session:
            return User.objects.get(id = request.session['userCurrent'])



def index(request):

    return render(request, "belt4/index.html")



def register(request):
    if request.method != 'POST':
        return redirect('/')
    test = User.objects.validUser(request.POST)

    if test['status'] == True:
        user = User.objects.userCreate(request.POST)
        request.session['userCurrent'] = user.id
        return redirect('/gotoTripManager')
    else:
        for error in test['Errors']:
            messages.add_message(request, messages.ERROR, error, extra_tags="register")
        return redirect('/')



def gotoTripManager(request):
    user = userInit(request)
    trips = user.plannedFor.all()
    userSchedule = []
    for trip in trips:
        userSchedule.append(trip.id)

    context = {
        'userCurrent': user,
        'trips': trips,
        'uTrips' : Destinations.objects.exclude(id__in = userSchedule)
    }

    return render(request, 'belt4/tripmanager.html', context)


def gotoAddTrip(request):

    return render(request, 'belt4/addTrip.html')


def login(request):
    if request.method != 'POST':
        return redirect('/')
    test = User.objects.checkUser(request.POST)
    if test['status'] == True:
        request.session['userCurrent'] = test['user'].id
        return redirect('/gotoTripManager')
    else:
        for error in test['Errors']:
		    messages.add_message(request, messages.ERROR, error, extra_tags="login")
        return redirect('/')



def logout(request):
    request.session.clear()

    return redirect('/')



def tripCreate(request):
    if request.method != 'POST':
        return redirect('/')
    test = Destinations.objects.validDest(request.POST, userInit(request))

    if test['status'] == True:
        dest = Destinations.objects.destCreator(request.POST, userInit(request))

        return redirect('/gotoTripManager')
    else:
        for error in test['Errors']:
		    messages.add_message(request, messages.ERROR, error, extra_tags="create")
        return redirect('/gotoTripManager')


def joinTrip(request, trip):
        user = userInit(request)
        dest = Destinations.objects.get(id = trip)
        dest.joinedBy.add(user)
        user.joined.add(dest)
        return redirect('/gotoTripManager')


def remove(request, destRemove):
    Destinations.objects.get(id = destRemove).delete()

    return redirect('/gotoTripManager')



def viewDestination(request, destination):
    desView = Destinations.objects.get(id = destination)
    print desView
    usersJoining = desView.joinedBy.all()
    print usersJoining

    context = {
        'dest' : desView,
        'users' : usersJoining
    }

    return render(request, "belt4/destination.html", context)
