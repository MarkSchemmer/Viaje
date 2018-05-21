from django.urls import path, re_path 
from . import views
urlpatterns=[
    path('', views.index, name='home'),
    path('join', views.join),
    path('reg', views.reg),
    path('login',views.login),
    path('success', views.success, name='success'),
    path('logout', views.logout),
    path('success/add_trip', views.add_trip, name='add_trip'),
    path('addTrip', views.add_trip_db),
    re_path(r'success/destination/(?P<id>\d+)', views.dest),
]