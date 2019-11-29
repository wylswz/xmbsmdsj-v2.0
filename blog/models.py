from django.db import models
import traceback,markdown2
from datetime import datetime
from taggit.managers import TaggableManager
# Create your models here.
from rest_framework.serializers import Serializer,SerializerMethodField
from rest_framework import serializers
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Blog(models.Model):
    def content_file_name(instance, filename):
        return 'blog/' + filename
    title = models.CharField(max_length=400, default='')
    abstract = models.CharField(max_length=1000,default='')
    content = models.TextField(max_length=400000, default='')
    cover = models.FileField(null=True,upload_to=content_file_name)
    cover_by = models.CharField(max_length=100, default="Anonymous")
    author = models.CharField(max_length=200,default='Y WEN')
    tags = TaggableManager()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def add_tags(self, tagstr):
        '''
        input
        @ tagstr: comma separated tags
        '''
        try:
            if tagstr is not None:
                tags = [a.lower() for a in tagstr.split(',')]
                print(tags)
                self.tags.set(*tags, clear=True)
                self.save()
        except Exception as e:
            traceback.print_exc()
        pass

    def get_tags(self):
        return self.tags.names()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-uploaded_at",)


class BlogSerializer(serializers.ModelSerializer):
    uploaded_at_formatted = serializers.SerializerMethodField('formatted_date')

    def formatted_date(self,foo):
        date = foo.uploaded_at

        return date.strftime('%b. %d, %Y, %p')
    class Meta:
        model = Blog
        fields = ('id','author','title','uploaded_at_formatted','abstract','cover','content','cover_by')

@receiver(post_delete, sender=Blog)
def submission_delete(sender, instance, **kwargs):
    instance.cover.delete(False)