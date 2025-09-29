from rest_framework import serializers
from .models import Photo,Album,PhotoView
from django.db.models import Sum
from django.urls import reverse

class PhotoSerializer(serializers.ModelSerializer):
  view_count = serializers.SerializerMethodField()
  class Meta:
    model = Photo
    fields = ["photo_name","photo_desc","photo_img","created_at","album","resolution","view_count"]
  def get_view_count(self, obj):
    return obj.views.aggregate(total=Sum("count"))["total"] or 0

class AlbumSerializer(serializers.ModelSerializer):
  photos = PhotoSerializer(many=True,read_only=True)
  album_link = serializers.SerializerMethodField()
  likes = serializers.SerializerMethodField()
  class Meta:
    model = Album
    fields = ["id","user","album_name","album_desc","created_at","photos","is_public","is_pinned","likes","album_link"]
    read_only_fields = ["user"]
    
  def get_album_link(self,obj):
    request = self.context.get("request")
    return request.build_absolute_uri(reverse('album',kwargs={'pk':obj.pk}))
  def get_likes(self,obj):
    return obj.likes.count()
  
class PhotoViewsSerializer(serializers.ModelSerializer):
  class Meta:
    model = PhotoView
    fields = ["count"]