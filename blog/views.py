from django.shortcuts import render
# Create your view
from rest_framework.response import Response
from utils.utils import token_auth
from rest_framework.decorators import api_view

from .models import Blog,BlogSerializer

import traceback,markdown2
import pygments


def blog(request):

    return render(request,'blog/blog.html')


@api_view(['POST'])
def fetch(request):
    try:
        start = int(request.POST.get('start'))
        number = int(request.POST.get('number'))
        blogs = Blog.objects.all()[start:start+number]
        blogs_ser = BlogSerializer(blogs,many=True).data

        return Response({"status":"success","blogs":blogs_ser})
    except Exception as e:
        traceback.print_exc()
        return Response({"status":"error","message":str(e)})


def detail(request,bid):
    try:
        my_extras = {
            'fenced-code-blocks': {'linenos': True}
        }
        blog = Blog.objects.get(id=bid)

        blog = BlogSerializer(blog).data
        print(blog)
        #md = markdown2.markdown(blog.get('content'),extras=my_extras)
        md = blog.get("content")
        return render(request,'blog/detail.html' ,context={"blog":blog,"md":md})
    except:
        return render(request,'patent/404.html')

@api_view(['POST','GET'])
@token_auth
def post(request):
    try:
        pass
        return Response({"status":"success"})
    except Exception as e:
        return Response({"status":"error","message":str(e)})

