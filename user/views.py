from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializer import UserSerializer
from .models import User


@api_view(['POST'])
def Register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data= request.data)

        if serializer.is_valid():
            serializer.save()

            return Response('User successfully registered!', status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
