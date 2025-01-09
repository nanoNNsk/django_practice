from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes

@api_view(['POST'])
def UserCreateApi(request):
    
    username = request.data['username']
    password = request.data['password']
    User.objects.create_user(username=username,password=password)
    return Response({
        'message' : 'user created'
    })

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProtectedView(request):
    return Response({
        'message' : 'Already authenticated',
        'username' : request.user.username
    })