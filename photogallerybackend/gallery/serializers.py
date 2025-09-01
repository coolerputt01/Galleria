from rest_framework import serializers
from .models import Photo,Album

class AlbumSerializer(serializers.ModelSerializer):
  photos = PhotoSerializer(many=True,read_only=True)
  class Meta:
    model = Album
    fields = ["id","user","album_name","album_desc","created_at","photos","is_public"]
    read_only_field("user")

class PhotoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Photo
    fields = ["photo_name","photo_desc","photo_img","created_at","album","resolution"]