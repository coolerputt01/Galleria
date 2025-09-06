from django.shortcuts import render
from rest_framework import permissions,generics
from rest_framework.views import APIView
from .serializers import PhotoSerializer,AlbumSerializer
from .models import Album, Photo,Likes,PhotoView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from accounts.permissions import IsUserVerifiedReadOnly
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework import status
# Create your views here.
class AlbumListCreateView(generics.ListCreateAPIView):
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
    user = self.request.user
    if serializer.validated_data.get("is_pinned", False):
      if Album.objects.filter(user=user, is_pinned=True).count() >= 5:
        raise ValidationError("You can only pin up to 5 albums.")
    serializer.save(user=user)

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
  queryset = Photo.objects.all()
  serializer_class = PhotoSerializer
  permission_classes = [IsUserVerifiedReadOnly]
  
class LikesView(APIView):
  permission_classes = [IsUserVerifiedReadOnly]
  def post(self,request,pk):
    album = get_object_or_404(Album,pk=pk)
    
    like,created = Likes.objects.get_or_create(user=request.user,album=album)
    if not created:
      like.delete()
      liked = False
    else:
      liked = True
    
    return Response({
      "likes": album.likes.count(),
      "is_liked":liked
    },status=status.HTTP_200_OK)
  
  def get(self,request,pk):
    photo = get_object_or_404(Photo,pk=pk)
    liked = photo.likes.filter(user=request.user).exists()
    return Response({
        "likes": album.likes.count(),
        "is_liked": is_liked
    }, status=status.HTTP_200_OK)
      
  
class PhotoViewed(APIView):
  permission_classes = [permissions.AllowAny]
  def post(self,request,pk):
    photo = get_object_or_404(Photo,pk=pk)
    
    photo_views ,created = PhotoView.objects.get_or_create(photo=photo)
    photo_views.count += 1
    photo_views.save()
    return Response({
      "photo":photo.photo_name,
      "views_count":photo_views.count,
    },status=status.HTTP_200_OK)