from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializer import UserSerializer
from .models import User

@api_view(['POST'])
def register_user(request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')

            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'},
                    status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'},
                    status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)