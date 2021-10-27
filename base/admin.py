from django.contrib import admin

# Register your models here.

from .models import Room,Topic,Message #Basically The database class we setup at models we areimporting it here


admin.site.register(Room) #Basically if you want to register the database you created to be used in the Admin pannel of django
admin.site.register(Topic) #Basically if you want to register the database you created to be used in the Admin pannel of django
admin.site.register(Message) #Basically if you want to register the database you created to be used in the Admin pannel of django

