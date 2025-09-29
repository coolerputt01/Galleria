from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
import io
from django.core.files.base import ContentFile

User = get_user_model()

# Create your models here.
class Album(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="album")
  album_name = models.CharField(default="Gallery",null=False,blank=False,max_length=30)
  album_desc = models.TextField(null=True,blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  is_pinned = models.BooleanField(default=False,null=False,blank=False)
  is_public = models.BooleanField(default=True,null=False,blank=False)
  
  def save(self,*args,**kwargs):
    if self.is_pinned:
      pinned_album_count = Album.objects.filter(user=self.user,is_pinned=True).exclude(pk=self.pk).count()
      if pinned_album_count >= 5:
        raise ValueError("You can only pin up to 5 albums.")
    super().save(*args, **kwargs)
    
  class Meta:
      unique_together = ("user","album_name")
  
  def __str__(self):
    return self.album_name
    
    
class Photo(models.Model):
  photo_name = models.CharField(default="Photo",blank=False,null=False,max_length=25)
  photo_desc = models.TextField(blank=True)
  photo_img = models.ImageField(upload_to='photos/',blank=False,null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  album = models.ForeignKey(Album,on_delete=models.CASCADE,related_name="photo")
  resolution = models.CharField(max_length=20)
  
  def save(self,*args,**kwargs):
    if self.photo_img:
      image = Image.open(self.photo_img)
      
      width,height = image.size
      image = image.resize((width * 2,height * 2), Image.LANCZOS)
      
      self.resolution = f"{width}px × {height}px"
      image_io = io.BytesIO()
      image.save(image_io, format="JPEG", quality=95)
      self.photo_img.save(self.photo_name, ContentFile(image_io.getvalue()), save=False)
      
      if not self.photo_name:
        img_count = Photo.objects.count() + 1
        self.photo_name = f"Photo {img_count}"
      super().save(*args, **kwargs)
  
  class Meta:
    unique_together = ("album","photo_name")
  
  def __str__(self):
    return self.photo_name
    
class Likes(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes")
  album = models.ForeignKey(Album,on_delete=models.CASCADE,related_name="likes")
  class Meta:
    unique_together = ("user","album")
    
  def __str__(self):
    return f"{self.user.display_name} liked {self.album.album_name}"
    
class PhotoView(models.Model):
  count = models.IntegerField(default=0,null=False,blank=False)
  photo = models.ForeignKey(Photo,on_delete=models.CASCADE,related_name="views")
  
  def __str__(self):
    return str(self.count)