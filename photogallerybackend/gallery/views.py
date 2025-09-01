from django.shortcuts import render
from rest_framework import permissions,generics
from .serializers import PhotoSerializer,AlbumSerializer
from .models import Album, Photo
from accounts.permissions import IsUserVerifiedReadOnly
# Create your views here.
class AlbumListCreateView(generics.generics.ListCreateAPIView):
  queryset = Album.objects.all()
  serializer_class = AlbumSerializer
  permission_classes = [IsUserVerifiedReadOnly]
  
  def get_queryset(self):
    user = self.request.user
    if user.is_authenticated:
      return Album.objects.filter(
          is_public=True
      ) | Album.objects.filter(user=user)
    else:
      return Album.objects.filter(is_public=True)
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = AlbumSerializer
    permission_classes = [IsUserVerifiedReadOnly]
    queryset = Album.objects.all()

class PhotoListCreateView(generics.ListCreateAPIView):
  queryset = Photo.objects.all()
  serializer_class = PhotoSerializer
  permission_classes = [IsUserVerifiedReadOnly]
  
  
  def get_queryset(self):
    user = self.request.user
    
    if user.is_authenticated:
      return Photo.objects.filter(album__is_public=True) | Photo.objects.filter(album__user=user)
    else:
        return Photo.objects.filter(album__is_public=True)

  def perform_create(self, serializer):
    album = serializer.validated_data.get("album")
    if album.user != self.request.user:
      raise PermissionDenied("You cannot add photos to someone else's album.")
    serializer.save()
  
  class PhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.object.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsUserVerifiedReadOnly]