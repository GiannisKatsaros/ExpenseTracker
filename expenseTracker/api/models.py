from django.db import models


# Create your models here.
class Expense(models.Model):
    account = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    transactionType = models.CharField(max_length=50)
    transactionDate = models.DateTimeField()
    valueDate = models.DateField()
    logisticBalance = models.DecimalField(max_digits=10, decimal_places=2)
    availableBalance = models.DecimalField(max_digits=10, decimal_places=2)
    description1 = models.TextField(blank=True)
    description2 = models.TextField(blank=True)
    importDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.description1} {self.description2} - {self.amount} {self.currency}"
        )
