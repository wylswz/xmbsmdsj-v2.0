from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from patent.settings import MEDIA_ROOT, MEDIA_URL
from functools import reduce
# Create your models here.
from PIL import Image as Img
import io as StringIO
import ast,traceback
import os

from rest_framework.serializers import Serializer,SerializerMethodField
from rest_framework import serializers
from taggit.managers import TaggableManager

class Photo(models.Model):

    def content_file_name(instance, filename):
        return 'gallery/' + filename

    title = models.CharField(max_length=400,null=False,default="UNKNOWN")
    summary = models.TextField(max_length=4000,null=True)
    file = models.FileField(upload_to=content_file_name, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    exif = models.CharField(max_length=4000,default='')
    tags = TaggableManager()
    author = models.CharField(max_length=400,default='Y WEN')
    views = models.IntegerField(default=0)

    def add_tags(self,tagstr):
        '''
        input
        @ tagstr: comma separated tags
        '''
        try:
            if tagstr is not None:
                tags = [a.lower() for a in tagstr.split(',')]
                print(tags)
                self.tags.set(*tags,clear=True)
                self.save()
        except Exception as e:
            traceback.print_exc()
        pass
    
    def get_tags(self):
        return self.tags.names()

    def get_thumbnail_path(self):
        split_name = str(self.file).split('.')
        thumbnail_name = MEDIA_ROOT + '/' + reduce(lambda x,y : x + y, split_name[:-1]) + '_thumbnail' + '.' +split_name[-1]
        thumbnail_dir = MEDIA_ROOT 
        thumbnail_url = MEDIA_URL + '/' + reduce(lambda x,y : x + y, split_name[:-1]) + '_thumbnail' + '.' +split_name[-1]
        if not os.path.isdir(thumbnail_dir):
            os.mkdir(thumbnail_dir)
        if not os.path.isfile(thumbnail_name):
            i = Img.open(self.file)
            i.thumbnail([i.size[0]/3, i.size[1]/3])
            i.save(thumbnail_name)
        return thumbnail_url

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-uploaded_at",)




class PhotoSerializer(serializers.ModelSerializer):
    tags = SerializerMethodField('tag_field')
    thumbnail = SerializerMethodField('thumbnail_field')

    def tag_field(self,foo):
        return foo.get_tags()

    def exif_field(self,foo):
        try:
            i = Img.open(MEDIA_ROOT + '/' + str(foo.file))
            exif = i._getexif()
            print(exif)
        except:
            traceback.print_exc()
    
    

    def thumbnail_field(self,foo):
        try:
            tp = foo.get_thumbnail_path()
            return tp
        except Exception as e:
            traceback.print_exc()
            return '' 


    class Meta:
        model = Photo
        fields = "__all__"
    
    



@receiver(post_delete, sender=Photo)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)
    