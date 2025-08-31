from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager

import uuid
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
  uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
  email = models.EmailField(unique=True)
  display_name = models.CharField(max_length=25,unique=True)
  pfp = models.ImageField(upload_to="pfps/",blank=True,null=True)
  bio = models.TextField(blank=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  
  objects = CustomUserManager();
  
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["display_name"]
  
  def __str__(self):
    return self.display_name