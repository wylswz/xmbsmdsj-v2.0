from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^detail/(?P<pid>\d+)/', views.detail, name='detail'),
    url(r'^upload_page/$', views.upload_page, name='upload_page'),
    url(r'^upload/5fea8a3f633ece767290e00d3afc5671/$', views.upload, name="upload"),
    url(r'^delete/5fea8a3f633ece767290e00d3afc5671/$', views.delete, name="delete"),
    url(r'^edit/5fea8a3f633ece767290e00d3afc5671/$', views.edit),
    url(r'^fetch/$', views.fetch,name='fetch'),
    url(r'^test/$', views.test, name='test'),
    

]
