from django.urls import reverse
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  
  class Meta:
    model = User
    fields = ['display_name','email','profileUrl','bio','password','pfp']
    
class PublicUserProfileSerializer(serializers.ModelSerializer):
  profile_url = serializers.SerializerMethodField()
  class Meta:
    model = User
    fields = ['display_name','email','bio','pfp','profile_url']
  def get_profile_url(self,user):
    request = self.context.get("request")
    return request.build_absolute_uri(reverse("public-profile",args=[str(user.display_name)]))