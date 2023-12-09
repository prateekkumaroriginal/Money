from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Sum

# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=200)
    amount = models.IntegerField()
    category = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name