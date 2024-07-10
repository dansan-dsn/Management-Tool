from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.mail import send_mail
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

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

            _user = serializer.save()

            refresh = RefreshToken.for_user(_user)
            access_token = refresh.access_token
            link = f'http://localhost/verify/{access_token}'

            # Send email with jwt token
            send_mail(
                'Registration Entry',
                f'Click to Login: {link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verify_user(request, token):
    try:
        refresh = RefreshToken(token)
        access_token = refresh.access_token
        _user = access_token.payload['user_id']
        new_user = User.objects.get(id=_user)

        if new_user.is_verified:
             return Response({'message': 'User already verified'}, status=status.HTTP_400_BAD_REQUEST)

        # mark user verified and save 
        new_user.is_verified = True
        new_user.save()

        return Response({'message': f'User {new_user.username} verified successfully'}, status=status.
        HTTP_200_OK)
    
    except TokenError:
        return Response({'error': 'Token is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)
    
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def refresh_token(request):
    refresh_token = request.data.get('refresh_token')

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return Response({'access_token': access_token}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)