from django.urls import path
from .views import getExpenses, createExpense, expenseDetail

urlpatterns = [
    path("expenses/", getExpenses, name="getExpenses"),
    path("expenses/create/", createExpense, name="createExpense"),
    path("expenses/<int:pk>/", expenseDetail, name="expenseDetail"),
]
