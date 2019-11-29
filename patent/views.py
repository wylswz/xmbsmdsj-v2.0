from django.shortcuts import render
from gallery.models import Photo
from .settings import MEDIA_URL
def index(request):
    context = {}
    p = Photo.objects.all()
    context['photos'] = p
    #context['media_url'] = MEDIA_URL

    return render(request, 'patent/index.html',context=context)

def about(request):
    return render(request, 'patent/about.html')