from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from . import views

from patent import settings

urlpatterns = [

    url(r'^$',views.blog,name='blog'),
    url(r'^fetch/$',views.fetch,name='fetch'),
    url(r'^detail/(?P<bid>\d+)/',views.detail,name='detail'),
    url(r'^edit/5fea8a3f633ece767290e00d3afc5671/$',views.post,name='post'),

]