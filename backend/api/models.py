from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    CATEGORY_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES)

    class Meta:
        unique_together = ('user', 'name', 'type')
        ordering = ['type', 'name']

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.type}: {self.amount} ({self.category})"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(help_text="First day of the month this budget applies to")

    class Meta:
        unique_together = ('user', 'category', 'month')
        ordering = ['-month']

    def __str__(self):
        return f"{self.category.name} - {self.amount} ({self.month.strftime('%B %Y')})"
