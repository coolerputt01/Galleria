from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serialisers import UserSerializer
from django.contrib.auth import authenticate

class SignupUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  permission_classes = [permissions.AllowAny]
  
class LoginUserView(APIView):
  def post(self,request):
    email = request.data['email']
    password = request.data['password']
    user = authenticate(email=email,password=password)
    if user:
      token = Token.get_or_create(user=user)
      return Response({
        "encrypted_virus": token.key
      },status=201)
    else:
      return Response({
        "error":"Credentials are Invalid"
      },status=401)
  