from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm): # form for room inherited
    class Meta:            # from ModelFrom
        model = Room
        fields = '__all__' # means meta data from model Room
                           # all fiels of Room (host,name, topic..)
        exclude = ['host', 'participants'] # now we won't see host and participants in form

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        #exclude = []