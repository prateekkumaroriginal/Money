from django.shortcuts import render
from django.views.generic import View, ListView, DetailView

# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'expenses/index.html')