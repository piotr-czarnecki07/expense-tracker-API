from rest_framework import status as st
from rest_framework.response import Response

from db_model.models import User
from views.userViews import hash_string

from functools import wraps
import json

def get_data(view):
    @wraps(view)
    def wrapper(request):
        if '_content' in request.data:
            request.data = json.loads(request.data['_content'])

        return view(request)

    return wrapper

def check_token(view):
    @wraps(view)
    def wrapper(request):
        if request.data.get('token') == None:
            return Response({'error': 'Token was not sent'}, status=st.HTTP_400_BAD_REQUEST)

        token = request.data['token']
        user = User.objects.filter(token=hash_string(token)).first()

        if user is None:
            return Response({'error': 'User with this token was not found. Maybe try logging in'}, status=st.HTTP_404_NOT_FOUND)
        
        request.user = user

        return view(request)

    return wrapper
