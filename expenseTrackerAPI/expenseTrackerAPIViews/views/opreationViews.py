from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as st

from django.core.exceptions import ValidationError
from django.db import DatabaseError

from db_model.models import Expense
from expenseTrackerAPIViews.serializers import ExpenseSerializer
from expenseTrackerAPIViews.decorators import get_data, check_token

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

@api_view(['POST'])
@check_token
@get_data
def addExpense(request):
    for param in ('title', 'amount', 'categories'):
        if param not in request.data:
            return Response({'error': 'Title, amount or categories field was not provided'}, status=st.HTTP_400_BAD_REQUEST)

    try:
        title = request.data['title']
        amount = float(request.data['amount'])
        categories = request.data['categories']

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
        return Response({'error': 'Title, amount or one of the catiegories is too long'}, status=st.HTTP_400_BAD_REQUEST)

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
    if 'expenses' not in request.data:
        return Response({'error': 'Expenses field is missing'}, status=st.HTTP_400_BAD_REQUEST)

    try:
        for expense in request.data['expenses']:
            if type(expense) is not dict:
                return Response({'error': 'Expense must be a json object'}, status=st.HTTP_400_BAD_REQUEST)

            if expense.get('id') is None:
                return Response({'error': 'Expense must contain an ID number'}, status=st.HTTP_400_BAD_REQUEST)
            else:
                expense['id'] = int(expense['id'])

    except ValueError:
        return Response({'error': 'ID must be an integer'}, status=st.HTTP_400_BAD_REQUEST)

    try:
        objects = []

        for expense in request.data['expenses']:
            expense_object = Expense.objects.filter(id=expense['id']).first()

            if expense_object is None:
                return Response({'error': f"Expense with ID {expense['id']} was not found"}, status=st.HTTP_404_NOT_FOUND)
            
            for param in ('title', 'amount', 'categories'):
                if param in expense:
                    if param == 'categories':
                        categories_names = []

                        for c in expense['categories']:
                            if c in categories_table.keys():
                                categories_names.append(categories_table.get(c))
                            else:
                                return Response({'error': f"Provided category number for expense with ID {expense['id']} is out of range (1-9)"}, status=st.HTTP_400_BAD_REQUEST)
                            
                        expense['categories'] = categories_names

                    setattr(expense_object, param, expense[param])

            expense_object.save()

            objects.append(expense_object)

        serializer = ExpenseSerializer(objects, many=True)

    except ValidationError:
        return Response({'error': 'Title, amount or one of the expenses is too long'}, status=st.HTTP_400_BAD_REQUEST)

    except DatabaseError as e:
        return Response({'error': f'Database error: {e}'}, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(serializer.data, status=st.HTTP_200_OK)

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
