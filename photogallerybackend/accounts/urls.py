from django.urls import path,include
from .views import SignupUserView,LoginUserView

urlpatterns = [
    path('signup/',LoginUserView.as_view(),name="signup"),
    path('login/',SignupUserView.as_view(),name="login"),
  ]