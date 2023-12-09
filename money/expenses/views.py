import json
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView, DeleteView
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum, DateTimeField
import datetime
from django.db.models.functions import TruncDate

# Create your views here.
class IndexView(View):
    template_name = 'expenses/index.html'

    def get(self, request):
        expense_form = ExpenseForm()
        expenses = Expense.objects.all()
        total_expenses = Expense.objects.aggregate(Sum('amount'))

        today = datetime.date.today()
        # last year sum
        last_year = today - datetime.timedelta(days=365)
        yearly_sum = Expense.objects.filter(date__gt=last_year, user=request.user).aggregate(Sum('amount'))

        # last month sum
        last_month = today - datetime.timedelta(days=30)
        monthly_sum = Expense.objects.filter(date__gt=last_month, user=request.user).aggregate(Sum('amount'))

        # last week sum
        last_week = today - datetime.timedelta(days=7)
        weekly_sum = Expense.objects.filter(date__gt=last_week, user=request.user).aggregate(Sum('amount'))

        year_start = datetime.date(today.year, 1, 1)
        month_start = datetime.date(today.year, today.month, 1)
        week_start = today - datetime.timedelta(days=today.weekday())

        # sums from since starting of...
        this_year_sum = Expense.objects.filter(date__gt=year_start, user=request.user).aggregate(Sum('amount'))
        this_month_sum = Expense.objects.filter(date__gt=month_start, user=request.user).aggregate(Sum('amount'))
        this_week_sum = Expense.objects.filter(date__gt=week_start, user=request.user).aggregate(Sum('amount'))

        daily_sums = Expense.objects.filter(user=request.user).annotate(
            truncated_date=TruncDate('date', output_field=DateTimeField())
        ).values('truncated_date').annotate(sum=Sum('amount')).order_by('-truncated_date')

        categorical_sums = Expense.objects.filter(user=request.user).values('category').annotate(sum=Sum('amount'))

        return render(request, self.template_name, {
            'expense_form': expense_form,
            'expenses': expenses,
            'total_expenses': total_expenses,
            'yearly_sum': yearly_sum,
            'monthly_sum': monthly_sum,
            'weekly_sum': weekly_sum,
            'this_year_sum': this_year_sum,
            'this_month_sum': this_month_sum,
            'this_week_sum': this_week_sum,
            'daily_sums': daily_sums,
            'categorical_sums': categorical_sums,
        })
       
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