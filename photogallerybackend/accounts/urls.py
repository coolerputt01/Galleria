from django.urls import path,include
from .views import SignupUserView,LoginUserView,PublicProfileView

urlpatterns = [
    path('auth/signup/',SignupUserView.as_view(),name="signup"),
    path('auth/login/',LoginUserView.as_view(),name="login"),
    path('profile/<str:display_name>/',PublicProfileView.as_view(),name="public-profile")
  ]