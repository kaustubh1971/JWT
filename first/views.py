from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt, datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
# Creating JWT token manually
from rest_framework_simplejwt.tokens import RefreshToken

class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=serializer.data['email'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'user_data':serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }) 


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        try:
            user_obj = User.objects.get(email=email)
        except:
            raise AuthenticationFailed("User Not Found")

        if not user_obj.check_password(password):
            raise AuthenticationFailed("Invalid Password")
        
        payload = {
            'id': user_obj.id,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now()
        }
        token = jwt.encode(payload, 'secret', algorithm="HS256")
        print(token)
        # return Response({
        #     "message":"Login Successful",
        #     "token": token
        # })
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token
        }
        return response


class UserDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            user_obj = User.objects.get(id=id)
        except:
            raise AuthenticationFailed("User Not Found")
        # serializer = UserSerializer(data=request.data)
        serializer = UserSerializer(user_obj)
        return Response(serializer.data) 
