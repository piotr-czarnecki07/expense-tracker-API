from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as st

from db_model.models import User, Expense
from expenseTrackerAPIViews.serializers import ExpenseSerializer

@api_view(['POST'])
def addExpense(request):
    pass

@api_view(['POST'])
def updateExpenses(request):
    pass

@api_view(['POST'])
def getExpenses(request):
    pass

@api_view(['POST'])
def deleteExpenses(request):
    pass