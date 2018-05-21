from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
import bcrypt
from  .models import * 

# Create your views here.
encrypt_password = lambda ps :  bcrypt.hashpw(ps.encode(), bcrypt.gensalt())
def index(request):
    return render(request, 'login_regis/index.html')

def reg(request):
    result = User.obj.registration(request.POST)
    if result['errors']:
        request.session['errors'] = result['errors']
        return redirect(reverse('home'))
    else:
        request.session['user_id'] = result['new_user'].id
        request.session['success'] = 'You have successfully in'
        return redirect(reverse('success'))

def login(request):
    result = User.obj.login(request.POST)
    if result['errors']:
        request.session['errors'] = result['errors']
        return redirect(reverse('home'))
    else:
        request.session['user_id'] = result['user'].id
        request.session['success'] = 'You have successfully logged in'
        return redirect(reverse('success'))



def logout(request):
    request.session.flush()
    return redirect(reverse('home'))

def success(request):
    user = User.obj.filter(id = request.session['user_id'])[0]
    my_trips = Trip.obj.filter(trip_creator=user)
    other_trips = Trip.obj.exclude(trip_creator=user).exclude(id__in=[o.id for o in list(user.users_joining.all())])
    my_other_trips = user.users_joining.all()
    
    return render(request, 'login_regis/success.html', {'user':user, 
                                                        'trips':my_trips, 
                                                        'other':other_trips, 
                                                        'my_other_trips':my_other_trips})


def add_trip(request):
    return render(request, 'login_regis/add_trip.html')


def add_trip_db(request):
    print(request.POST)
    result = Trip.obj.create_trip(request.POST)
    print(result['errors'])
    if result['errors']:
        request.session['errors'] = result['errors']
        return redirect(reverse('add_trip'))
    else:
        return redirect(reverse('success'))



def dest(request, id):
    print(id)
    trip = Trip.obj.get(id=id)
    user = User.obj.get(trips=id)
    others = trip.users_joined.all()
    context={'trip':trip, 'user':user, 'other_users':others}
    return render(request, 'login_regis/dest.html', context)


def join(request):
    print(request.POST)
    get_trip = Trip.obj.get(id=request.POST['trip_id'])
    this_user = User.obj.filter(id = request.session['user_id'])[0]
    get_trip.users_joined.add(this_user)
    return redirect(reverse('success'))
