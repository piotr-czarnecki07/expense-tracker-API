from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as st

from django.core.exceptions import ValidationError
from django.db import DatabaseError

from db_model.models import User, Expense
from expenseTrackerAPIViews.serializers import ExpenseSerializer
from expenseTrackerAPIViews.decorators import get_data, check_token

import json

@api_view(['POST'])
@check_token
@get_data
def addExpense(request):
    for param in ('title', 'amount', 'categories'):
        if param not in request.data:
            return Response({'error': 'Title, amount or categories field was not provided'}, status=st.HTTP_400_BAD_REQUEST)

    categories_table = {
        1: 'Groceries',
        2: 'Leisure',
        3: 'Electronics',
        4: 'Utilities',
        5: 'Clothing',
        6: 'Health',
        7: 'School',
        8: 'Home',
        9: 'Other'
    }

    try:
        title = request.data['title']
        amount = float(request.data['amount'])
        categories = json.loads(request.data['categories'])

        categories_names = []

        for c in categories:
            if c in categories_table.keys():
                categories_names.append(categories_table.get(c))
            else:
                return Response({'error': 'Category number out of range (1-9)'}, status=st.HTTP_400_BAD_REQUEST)

        expense = Expense(title=title, amount=amount, categories=categories_names)
        expense.save()

        request.user.expenses.append(expense.id)
        request.user.save()

        serializer = ExpenseSerializer(expense)

    except ValidationError:
        return Response({'error': 'Username or email are too long'}, status=st.HTTP_400_BAD_REQUEST)

    except DatabaseError as e:
        return Response({'error': f'Database error: {e}'}, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

    except (KeyError, ValueError):
        return Response({'error': 'Request body is invalid. Parameters are of wrong data type'}, status=st.HTTP_400_BAD_REQUEST)

    else:
        return Response(serializer.data, status=st.HTTP_201_CREATED)

@api_view(['POST'])
@check_token
@get_data
def updateExpenses(request):
    pass

@api_view(['POST'])
@check_token
@get_data
def getExpenses(request):
    pass

@api_view(['POST'])
@check_token
@get_data
def deleteExpenses(request):
    pass