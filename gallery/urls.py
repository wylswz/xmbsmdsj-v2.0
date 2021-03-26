from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^detail/(?P<pid>\d+)/', views.detail, name='detail'),
    url(r'^fetch/$', views.fetch,name='fetch'),
    url(r'^test/$', views.test, name='test'),
]
