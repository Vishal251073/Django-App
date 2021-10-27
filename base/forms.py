from django.forms import ModelForm, fields
from django.contrib.auth.models import User
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' # We are Basically Inheriting the Room database from model and using __all__ we passing all the fields to
        #django and using its builtin Functionality django will creste from for us
        exclude = ['host','participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']