from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager
from django.utils import timezone
from datetime import timedelta
import uuid
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
  uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
  email = models.EmailField(unique=True)
  display_name = models.CharField(max_length=25,unique=True)
  pfp = models.ImageField(upload_to="pfps/",blank=True,null=True)
  bio = models.TextField(blank=True)
  is_verified = models.BooleanField(default=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  
  objects = CustomUserManager();
  
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["display_name"]
  
  def __str__(self):
    return self.display_name
    
class VerificationToken(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="verification_tokens")
  token = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  expires_at = models.DateTimeField()
  
  def is_expired(self):
    return timezone.now() > self.expires_at
  @classmethod
  def create_token(cls, user, expiry_minutes=5):
    return cls.objects.create(user=user,expires_at=timezone.now() + timedelta(minutes=expiry_minutes))
  
class Badge(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")
   badge_name = models.CharField(blank=False, null=False, max_length=25)
   badge_photo = models.CharField(blank=False, null=False, max_length=50)
    
   class Meta():
     unique_together = ("user","badge_name")
      
   def __str__(self):
        return f"{self.badge_name}"
     
class Theme(models.Model):
  name = models.CharField(blank=False,null=False,max_length=25)
  primary_color = models.CharField(blank=False,null=False,max_length=7)
  secondary_color = models.CharField(blank=False,null=False,max_length=7)
  
  def __str__(self):
    return f"{self.name}"

class UserTheme(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="theme")
  theme = models.ForeignKey(Theme,on_delete=models.CASCADE,related_name="Theme")
  
  def __str__(self):
    return f"{self.user} has {self.theme}"