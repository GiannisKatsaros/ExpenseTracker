from django.urls import path
from .views import ExpensesView

# from .views import getExpenses, createExpense, expenseDetail

expenses_view = ExpensesView.as_view()

urlpatterns = [
    # path("expenses/", getExpenses, name="getExpenses"),
    # path("expenses/create/", createExpense, name="createExpense"),
    # path("expenses/<int:pk>/", expenseDetail, name="expenseDetail"),
    path(
        "expenses/import/",
        expenses_view,
        {"action": "import_expenses"},
        name="import_expenses",
    ),
]
