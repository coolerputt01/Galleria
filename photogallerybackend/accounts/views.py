from rest_framework import generics,permissions,status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serialisers import UserSerializer,PublicUserProfileSerializer
from .models import User, VerificationToken
from django.contrib.auth import authenticate

class SignupUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  permission_classes = [permissions.AllowAny]
  def perform_create(self,serializer):
    user = serializer.save(is_verified=False)
    token = VerificationToken.create_token(User)
  
class LoginUserView(APIView):
  permission_classes = [permissions.AllowAny]
  def post(self,request):
    email = request.data['email']
    password = request.data['password']
    user = authenticate(email=email,password=password)
    if user:
      token , create= Token.objects.get_or_create(user=user)
      return Response({
        "encrypted_virus": token.key
      },status=200)
    else:
      return Response({
        "error":"Credentials are Invalid"
      },status=401)
  
class PublicProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    lookup_field = "display_name"
    
    def get_object(self):
      try:
        return super().get_object()
      except Exception:
        raise NotFound(detail="The user you are looking for is not available.")
        
class VerifyUserToken(APIView):
  permission_classes = [permissions.AllowAny]
  def get(self, request,token):
    try:
      token = VerificationToken.objects.get(token=token)
    except VerificationToken.DoesNotExist:
      return Response({
        "error":"Verfication Link does not exist"
      },status=status.HTTP_400_BAD_REQUEST)
    
    if token.is_expired():
      return Response({
        "error":"Verification Link is expired"
      },status=status.HTTP_400_BAD_REQUEST)
    user = token.user
    user.is_verified = True
    user.save()
    token.delete()
    
    return Response({
      "success":"Account Successfully Verified"
    },status=status.HTTP_200_OK) 