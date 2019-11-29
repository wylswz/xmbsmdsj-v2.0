from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie,requires_csrf_token
from .models import Photo,PhotoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from PIL import Image
import traceback, ast, json
from patent.settings import hash,MEDIA_URL,MEDIA_ROOT


from utils.utils import token_auth,image_compress




def detail(request,pid):
    context = {}
    try:
        photo = Photo.objects.get(id=int(pid))
        context['photo'] = photo
        context['tags'] = photo.get_tags()

    except Exception as e:
        print(e)
        return render(request,'patent/404.html')

    return render(request,'gallery/single-blog.html',context=context)


@ensure_csrf_cookie
def upload_page(request):
    return render(request, 'gallery/photo-upload.html')


@api_view(['POST'])
@token_auth
def upload(request):
    try:
        file = request.FILES.get("file")
        title = request.POST.get("title")
        summary = request.POST.get("summary")
        tags = str(request.POST.get("tags"))
        author = str(request.POST.get("author"))

        if file is None:
            return Response({"status":"error", "message":"Image file cannot be empty"})

        photo = Photo()
        photo.summary = summary
        photo.file = file
        photo.title = title
        if author is not None:
            photo.author = author
        photo.save()
        photo.add_tags(tags)
        exif = image_compress(MEDIA_ROOT + '/' + str(photo.file),MEDIA_ROOT + '/' + str(photo.file))
        photo.exif = exif
        photo.save()
        return Response({"status": "success"})
    except Exception as e:
        traceback.print_exc()
        return Response({"status": "error"})

@api_view(["POST"])
@token_auth
def delete(request):
    try:
        id = request.POST.get("id")
        Photo.objects.filter(id=int(id)).delete()
        return Response({"status": "success"})
    except Exception as e:
        return Response({"status": "error","message":str(e)})


@api_view(["POST"])
@token_auth
def edit(request):
    try:
        id = request.POST.get("id")
        tags = str(request.POST.get("tags"))
        new_title = request.POST.get("title")
        new_summary = request.POST.get("summary")
        photo = Photo.objects.get(id=int(id))
        photo.title = new_title
        photo.summary = new_summary
        photo.save()
        photo.add_tags(tags)
        return Response({"status": "success"})
    except Exception as e:
        return Response({"status": "error","message":str(e)})

@api_view(["POST"])
def fetch(request):
    try:
        start = int(request.POST.get("start"))
        number = int(request.POST.get("number"))

        photos = Photo.objects.all()[start:start+number]
        photos_json = PhotoSerializer(photos,many=True).data
        return Response({"status":"success", "photos":photos_json})
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