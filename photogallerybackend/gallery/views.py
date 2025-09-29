from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied

from .models import Album, Photo, Likes, PhotoView
from .serializers import AlbumSerializer, PhotoSerializer
from accounts.permissions import IsUserVerifiedReadOnly


# ------------------ Album Views ------------------ #
class AlbumListCreateView(generics.ListCreateAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [IsUserVerifiedReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Album.objects.filter(is_public=True)
        if user.is_authenticated:
            queryset = queryset | Album.objects.filter(user=user)

        # Search
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                models.Q(album_name__icontains=search_query) |
                models.Q(album_desc__icontains=search_query)
            )

        # Sorting
        sort_by = self.request.query_params.get('sort', 'created_at')  # default: newest first
        if sort_by == 'likes':
            queryset = sorted(queryset, key=lambda a: a.likes.count(), reverse=True)
        elif sort_by == 'name':
            queryset = queryset.order_by('album_name')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

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


# ------------------ Photo Views ------------------ #
class PhotoListCreateView(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsUserVerifiedReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Photo.objects.filter(album__is_public=True)
        if user.is_authenticated:
            queryset = queryset | Photo.objects.filter(album__user=user)

        # Search
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                models.Q(photo_name__icontains=search_query) |
                models.Q(photo_desc__icontains=search_query)
            )

        # Sorting
        sort_by = self.request.query_params.get('sort', 'created_at')
        if sort_by == 'views':
            queryset = sorted(queryset, key=lambda p: sum(v.count for v in p.views.all()), reverse=True)
        elif sort_by == 'name':
            queryset = queryset.order_by('photo_name')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def perform_create(self, serializer):
        album = serializer.validated_data.get("album")
        if album.user != self.request.user:
            raise PermissionDenied("You cannot add photos to someone else's album.")
        serializer.save()


class PhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsUserVerifiedReadOnly]


# ------------------ Likes Views ------------------ #
class AlbumLikesView(APIView):
    permission_classes = [IsUserVerifiedReadOnly]

    def post(self, request, pk):
        album = get_object_or_404(Album, pk=pk)
        like, created = Likes.objects.get_or_create(user=request.user, album=album)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return Response({
            "likes": album.likes.count(),
            "is_liked": liked
        }, status=status.HTTP_200_OK)


# ------------------ Photo Views Counter ------------------ #
class PhotoViewed(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        photo_views, created = PhotoView.objects.get_or_create(photo=photo)
        photo_views.count += 1
        photo_views.save()

        return Response({
            "photo": photo.photo_name,
            "views_count": photo_views.count,
        }, status=status.HTTP_200_OK)