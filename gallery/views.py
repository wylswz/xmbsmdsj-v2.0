from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import ensure_csrf_cookie,requires_csrf_token
from .models import Photo
from .services import ImageService
from patent.settings import hash, MEDIA_URL, MEDIA_ROOT, GALLERY_META

from rest_framework.decorators import api_view
from rest_framework.response import Response
from PIL import Image
import traceback, ast, json
import os

# Assume I can never upload more than 1024 photos
MAX_NUM = 1024


def detail(request, pid):
    context = {}
    try:
        image_metas = ImageService.load_image_metas(0, MAX_NUM)
        for meta in image_metas:
            if meta.id == int(pid):
                context['photo'] = meta.serialize()
                context['photoStr'] = json.dumps(meta.serialize())
                context['tags'] = meta.tags

    except Exception as e:
        print(e)
        return render(request,'patent/404.html')

    return render(request,'gallery/single-blog.html',context=context)



@api_view(["POST"])
def fetch(request):
    try:
        start = int(request.POST.get("start"))
        number = int(request.POST.get("number"))
        image_metas = ImageService.load_image_metas(start, number)
        return Response({
            'photos': [i.serialize() for i in image_metas]
        })
    except Exception as e:
        return Response({"status": "error","message":str(e)})


@api_view(["POST"])
def test(request):
    try:
        p = Photo.objects.all()[0]
        thumbnail = p.get_thumbnail_path()

        return Response({"status":"success", "output":thumbnail})
    except IndexError:

        return Response({"status":"Error", "message":"Please test after uploading at least one image"})