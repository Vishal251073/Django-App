# from functools import _Descriptor
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
# Create your models here.
#Here we handle our Databases


#Now we will make model for Topics
# class Avatar(User):
#     avatar = models.ImageField(null=True,default="avatar.svg")

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host=models.ForeignKey(User,on_delete=SET_NULL,null=True)
    #Host will be the one who created the room by sigining in
    topic=models.ForeignKey(Topic,on_delete=SET_NULL,null=True) #Two important notes
    #Note 1 if the model that we are rendering here i.e topic is declared below this code we have to wrap the Topic as 'Topic'
    #Note 2 On deleting the topic we want to keep the Room we are seting on_delete to setnull but to render this in database we have to keep null as true also
    #The type of relationship we will incorporate depends on our needs Basically a Topic can have multiple rooms but 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True) #null is true of for example a user make a room and don't want to add some description at that point so that true will allow to do so
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name

#Now we will be creating a model of one to many Relationship Type to keep the message of a single user

class Message(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    #This user relationship is also one to many type of datbase as one user will have multiple messages
    #Also we are using builtin Model of  Django User 
    room = models.ForeignKey(Room , on_delete=models.CASCADE)
    #Basically Cascade will do is that it will delete all the childrens of the particular room when it get deleted
    #If we have used SET_NULL it would have keep the mesages with it
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']
    def __str__(self):
        return self.body[0:50]