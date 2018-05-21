#from __future__ import unicode_literals
from django.db import models
import bcrypt
import re as r 
import datetime 
# Create your models here.
re_email = r.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

re_date = r.compile(r'^\d{4}-\d{2}-\d{2}$')

class ClassManager(models.Manager):
    def registration(self,obj):
        results = {}
        errors = {}
        if len(obj['first_name']) < 2 :
            errors['first_name'] = 'first name cannot be lesser than 2 chars'
        if  len(obj['ps']) < 8 : 
            errors['ps'] = ['password must be greater than 8 chars']
        if obj['ps'] != obj['psconf'] :
            errors['ps'] = 'password must match confirmation passowrd'

        if len(errors) == 0:
            ps = obj['ps']
            hash_ps = bcrypt.hashpw(ps.encode(), bcrypt.gensalt()).decode('utf-8')
            print(hash_ps)
            results['new_user'] = self.create(first_name=obj['first_name'], email=obj['email'], password=hash_ps)
        results['errors'] = errors
        return results
    def login(self,post_data):
        results = {}
        errors = {}
        inputPass = post_data['ps']
        user = User.obj.filter(email=post_data['email'])
        if len(post_data['ps']) < 2 or len(post_data['email']) < 5:
            errors['login_error'] = 'login error' 
        if not user:
            errors['login_error'] = 'Login error'
        elif not bcrypt.checkpw(inputPass.encode('utf-8'), user[0].password.encode('utf-8')):
            errors['login_error'] = 'Login error'
        results['errors'] = errors
        if len(errors) == 0:
            results['user'] = user[0]
        return results

class TripManager(models.Manager):
    def create_trip(self, post_data):
        results = {}
        errors = {}
        this_user = User.obj.get(id=post_data['user'])
        current_date = datetime.datetime.now()
        if len(post_data['destination']) < 8 or len(post_data['description']) < 8:
            errors['emp'] = 'all fields must be filled in and longer than 8 chars'
        if not re_date.match(post_data['date']) or not re_date.match(post_data['enddate']):
            errors['date'] = 'Please format date properly'
            results['errors'] = errors
            return results
        start_date_times = [int(x) for x in post_data['date'].split('-')]
        end_date_times = [int(x) for x in post_data['enddate'].split('-')]
        start_date = datetime.datetime(start_date_times[0], start_date_times[1], start_date_times[2])
        end_date = datetime.datetime(end_date_times[0], end_date_times[1], end_date_times[2])
        if start_date < current_date:
            errors['date'] = 'start date must be scheduled in the future'
        if start_date > end_date:
            errors['date'] = 'Please schedule end date after start date'
        results['errors'] = errors
        if len(errors) == 0 :
            results['trip'] = self.create(
                destination=post_data['destination'], 
                description=post_data['description'], 
                traval_start_date=start_date, 
                traval_end_date=end_date,
                trip_creator=this_user
                )
        return results
            
            

''' 

import datetime 


d = datetime.datetime(Year, Month, Day)

then you can compare dates with > or < signs 

also this can be used for validation!



'''


'''


Need to query for logged in users trips!

need to query for all other trips exlcuding the logged in user!


'''

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    obj = ClassManager()



class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    traval_start_date = models.DateTimeField()
    traval_end_date = models.DateTimeField()
    trip_creator = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE)
    users_joined = models.ManyToManyField(User, related_name='users_joining')
    obj = TripManager()

