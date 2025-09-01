from django.urls import path
from .views import AlbumListCreateView,AlbumDetailView,PhotoListCreateView,PhotoDetailView

urlpatterns = [
  path('albums/',AlbumListCreateView.as_view(),name="albums-get-create"),
  path('albums/<int:pk>/',AlbumDetailView.as_view(),name="album"),
  path('photos',PhotoListCreateView.as_view(),name="photos-get-create"),
  path('photos/<int:pk>/',PhotoDetailView.as_view(),name="photo")
  ]