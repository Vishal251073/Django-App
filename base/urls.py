from collections import namedtuple
from django.core.exceptions import ViewDoesNotExist
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"), # The reason of using name keyword to fix the path to receive it for example if we change it in future to any other path we don't need to update it anywhere as it will be still named as name
    path('room/<str:pk>',views.room, name="room"), #pk here is prrimary key i.e similar to the new path made by user similar to ejs templating
    path('profile/<str:pk>',views.userProfile,name='user-profile'),
    path('create-room/', views.createRoom,name = "create-room"),
    path('update-room/<str:pk>', views.updateRoom,name = "update-room"),
    path('delete-room/<str:pk>', views.deleteRoom,name = "delete-room"),
    path('login/',views.loginPage,name = "login"),
    path('logout/',views.logOutUser,name = "logout"),
    path('register/',views.registerUser,name = "register"),
    path('delete-message/<str:pk>',views.deleteMessage,name = "delete-message"),
    path('update-user/',views.updateUser,name = "update-user"),
    path('topics/',views.topicsPage,name = "topics"),
    path('activity/',views.activityPage,name = "activity")
]