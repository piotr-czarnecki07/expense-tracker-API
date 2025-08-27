from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as st
from expenseTrackerAPIViews.decorators import get_data

@api_view(['POST'])
@get_data
def signup(request):
    pass

@api_view(['POST'])
@get_data
def login(requset):
    pass

@api_view(['POST'])
@get_data
def remindToken(request):
    pass

@api_view(['POST'])
@get_data
def logout(request):
    pass
