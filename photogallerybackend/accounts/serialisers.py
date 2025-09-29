from django.urls import reverse
from rest_framework import serializers
from .models import User,Theme,UserTheme,Badge

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  
  class Meta:
    model = User
    fields = ['display_name','email','bio','password','pfp']
    
class PublicUserProfileSerializer(serializers.ModelSerializer):
  profile_url = serializers.SerializerMethodField()
  class Meta:
    model = User
    fields = ['display_name','email','bio','pfp','profile_url']
  def get_profile_url(self,user):
    request = self.context.get("request")
    return request.build_absolute_uri(reverse("public-profile",args=[str(user.display_name)]))

class ThemeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Theme
    fields = ["id","name","primary_color","secondary_color"]

class UserThemeSerializer(serializers.ModelSerializer):
  theme = ThemeSerializer(read_only=True)
  theme_id = serializers.PrimaryKeyRelatedField(
        queryset=Theme.objects.all(),
        source="theme", write_only=True)
  class Meta:
        model = UserTheme
        fields = ["user", "theme", "theme_id"]
        read_only_fields = ["user"]
  def create(self,obj):
    user = self.context["request"].user
    theme = validated_data.get("theme")
    obj, created = UserTheme.objects.update_or_create(user=user, defaults={"theme": theme})
    return obj
  
class BadgeSerializer():
  class Meta():
    model = Badge
    fields = ["user","badge_name","badge_photo"]