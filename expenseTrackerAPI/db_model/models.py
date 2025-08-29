from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=20)

    expenses = models.JSONField(default=list)

    token = models.CharField(max_length=50)

    createdAt = models.DateField(auto_now_add=True)

class Expense(models.Model):
    title = models.CharField(max_length=50)
    amount = models.FloatField()
    categories = models.JSONField(default=list)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
