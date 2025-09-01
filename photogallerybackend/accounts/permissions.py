from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsUserVerifiedReadOnly(BasePermission):
  def has_permission(self,request,view):
    if request.method in SAFE_METHODS:
      return True
    return request.user and request.user.isAuthenticated and request.user.is_verified
  def has_object_permission(self, request, view, obj):
    if request.method in SAFE_METHODS:
      return obj.is_public or obj.user == request.user
    return obj.user == request.user