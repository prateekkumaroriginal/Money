from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, UpdateView, DeleteView
from .forms import ExpenseForm
from .models import Expense

# Create your views here.
class IndexView(View):
    template_name = 'expenses/index.html'

    def get(self, request):
        expense_form = ExpenseForm()
        expenses = Expense.objects.all()
        return render(request, self.template_name, {'expense_form': expense_form, 'expenses': expenses})
       
    def post(self, request):
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('index')
        expenses = Expense.objects.all()
        return render(request, self.template_name, {'expense_form': expense_form, 'expenses': expenses})

class ExpenseUpdateView(UpdateView):
    model = Expense
    fields = ['name', 'amount', 'category']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('index')

class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy('index')