from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as st
from django.core.exceptions import ValidationError
from django.db import DatabaseError

from expenseTrackerAPIViews.decorators import get_data, check_token
from db_model.models import User

from expenseTrackerAPIViews.hashes import HASH_TABLE, DEHASH_TABLE
import random

def generate_token() -> str:
    token = ''
    for _ in range(50):
        token += random.choice(list(HASH_TABLE.keys()))

    return token

def hash_string(string: str) -> str:
    new_string = ''
    for i in string:
        new_string += HASH_TABLE[i]

    return new_string

def dehash_string(string: str) -> str:
    new_string = ''
    for i in string:
        new_string += DEHASH_TABLE[i]

    return new_string

@api_view(['POST'])
@get_data
def signup(request):
    for param in ('username', 'email', 'password'):
        if param not in request.data:
            return Response({'error': 'Username, email or password is missing'}, status=st.HTTP_400_BAD_REQUEST)

    username = request.data['username']
    email = request.data['email']
    password = request.data['password']

    if len(password) > 20:
        return Response({'error': 'Password is too long'}, status=st.HTTP_400_BAD_REQUEST)

    for i in password:
        if i not in HASH_TABLE.keys():
            return Response({'error': 'Password contains forbidden symbols. Use only from: a-z, A-Z, 0-9, !@#$%^&*()'}, status=st.HTTP_400_BAD_REQUEST)

    token = generate_token()

    try:
        if User.objects.filter(email=request.data['email']).first() is not None:
            return Response({'error': 'This email is already taken'}, status=st.HTTP_400_BAD_REQUEST)
        user = User(username=username, email=email, password=hash_string(password), token=hash_string(token), expenses=[])
        user.save()

    except ValidationError:
        return Response({'error': 'Username or email are too long'}, status=st.HTTP_400_BAD_REQUEST)

    except DatabaseError as e:
        return Response({'error': f'Database error: {e}'}, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

    except (KeyError, ValueError):
        return Response({'error': 'Request body is invalid. Parameters are of wrong data type'}, status=st.HTTP_400_BAD_REQUEST)

    else:
        return Response({'token': token}, status=st.HTTP_201_CREATED)

@api_view(['POST'])
@get_data
def login(request):
    for param in ('email', 'password'):
        if param not in request.data:
            return Response({'error': 'Email or password is missing'}, status=st.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.filter(email=request.data['email']).first()

        if user is None:
           return Response({'error': 'This email is not assigned to any user'}, status=st.HTTP_404_NOT_FOUND)

        if user.password != hash_string(request.data['password']):
            return Response({'error': 'Password is incorrect'}, status=st.HTTP_403_FORBIDDEN)

        token = generate_token()

        user.token = hash_string(token)
        user.save()

    except ValidationError:
        return Response({'error': 'Email or password are too long'}, status=st.HTTP_400_BAD_REQUEST)

    except DatabaseError as e:
        return Response({'error': f'Database error: {e}'}, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

    except (KeyError, ValueError):
        return Response({'error': 'Request body is invalid. Parameters are of wrong data type'}, status=st.HTTP_400_BAD_REQUEST)

    else:
        return Response({'token': token}, status=st.HTTP_200_OK)

@api_view(['POST'])
@get_data
def remind_token(request):
    for param in ('email', 'password'):
        if param in request.data:
            return Response({'error': 'Email or password is missing'}, status=st.HTTP_400_BAD_REQUEST)
        
    try:
        user = User.objects.filter(email=request.data['email']).first()

        if user is None:
           return Response({'error': 'This email is not assigned to any user'}, status=st.HTTP_404_NOT_FOUND)

        if user.password != hash_string(request.data['password']):
            return Response({'error': 'Password is incorrect'}, status=st.HTTP_403_FORBIDDEN)
        
        if user.token == 'logged_out':
            return Response({'message': 'User is not logged in'}, status=st.HTTP_200_OK)

        token = dehash_string(user.token)

    except ValidationError:
        return Response({'error': 'Username or email are too long'}, status=st.HTTP_400_BAD_REQUEST)

    except DatabaseError as e:
        return Response({'error': f'Database error: {e}'}, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

    except (KeyError, ValueError):
        return Response({'error': 'Request body is invalid. Parameters are of wrong data type'}, status=st.HTTP_400_BAD_REQUEST)

    else:
        return Response({'token': token}, status=st.HTTP_200_OK)

@api_view(['POST'])
@check_token
@get_data
def logout(request):
    try:
        request.user.token = 'logged_out'
        request.user.save()

    except DatabaseError as e:
        return Response({'error': f'Database error: {e}'}, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response({'message': 'User logged out successfully'}, status=st.HTTP_200_OK)
