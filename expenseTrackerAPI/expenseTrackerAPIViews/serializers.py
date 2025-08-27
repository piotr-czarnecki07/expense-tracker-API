from db_model.models import Expense
from rest_framework.serializers import ModelSerializer

class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
