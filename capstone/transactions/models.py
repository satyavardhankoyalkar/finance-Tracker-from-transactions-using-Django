from django.db import models

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]
    SUBCATEGORY_CHOICES = [
        ('Rent', 'Rent'),
        ('Food', 'Food'),
        ('Entertainment', 'Entertainment'),
        ('Salary', 'Salary'),
        ('Utilities', 'Utilities'),
        # Add other subcategories as needed
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(
        max_length=20,
        choices=SUBCATEGORY_CHOICES,
        blank=True,  # Subcategory is optional for Income
        null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.subcategory:
            return f"{self.category} ({self.subcategory}) - {self.amount} on {self.date}"
        return f"{self.category} - {self.amount} on {self.date}"
