from django.shortcuts import render
from gallery.models import Photo
from gallery.services import ImageService
from .settings import MEDIA_URL



def index(request):
    context = {}
    p = ImageService.load_image_metas()

    context['photos'] = [i.serialize() for i in p]
    #context['media_url'] = MEDIA_URL

    return render(request, 'patent/index.html',context=context)

def about(request):
    return render(request, 'patent/about.html')