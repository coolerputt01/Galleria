from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
  def create_user(self, email,password=None,display_name=None,**extra_fields):
    if not email:
      raise ValueError(_(f"Email Field must be set lol."))
    email = self.normalize_email(email)
    user = self.model(email=email,display_name=display_name,**extra_fields)
    
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self,email,password=None,**extra_fields):
    extra_fields.setdefault("is_staff",True)
    extra_fields.setdefault("is_superuser",True)
    extra_fields.setdefault("is_active",True)
    
    if extra_fields.get("is_staff") is not True:
      raise ValueError(_('Super_user must have "is_staff" field = True'))
    if extra_fields.get("is_superuser") is not True:
      raise ValueError(_('Super_user must have "is_superuser" field = True'))
      
    extra_fields.pop("display_name",None)
    return self.create_user(email,password,display_name="admin",**extra_fields)