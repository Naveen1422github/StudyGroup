# login required

> now to use this functionality we import login_required

> and now we can use this on any fn

   @login_required(login_url='login')
   def createRoom(request):
   .
   .
   .

> now to create room we have to have login

# inluding css

> to this we made a static folder main folder inside this there
> are folders styles for css and images for image

> now to make django know about this folder we have to do something in settings.py 

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

> inside main.html we have to load static

{% load static%}

and hrf in linking stylesheet

href="{% static 'styles/main.css' %}"
