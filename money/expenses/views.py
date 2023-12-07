from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from .forms import ExpenseForm
from .models import Expense

# Create your views here.
class IndexView(View):
    def get(self, request):
        expense_form = ExpenseForm()
        expenses = Expense.objects.all()
        return render(request, 'expenses/index.html', {'expense_form': expense_form, 'expenses': expenses})
    
    def post(self, request):
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense_form.save()
            return render(request, 'expenses/index.html', {'expense_form': ExpenseForm()})
        return render(request, 'expenses/index.html', {'expense_form': expense_form})
