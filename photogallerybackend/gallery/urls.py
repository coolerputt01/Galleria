from django.urls import path
from .views import AlbumListCreateView,AlbumDetailView,PhotoListCreateView,PhotoDetailView,PhotoViewed,LikesView

urlpatterns = [
  path('albums/',AlbumListCreateView.as_view(),name="albums-get-create"),
  path('albums/<int:pk>/',AlbumDetailView.as_view(),name="album"),
  path('photos/',PhotoListCreateView.as_view(),name="photos-get-create"),
  path('photos/<int:pk>/',PhotoDetailView.as_view(),name="photo"),
  path('photo/<int:pk>/view/',PhotoViewed.as_view(),name="photo-view"),
  path('album/<int:pk>/like/',LikesView.as_view(),name="photo-like")
  ]