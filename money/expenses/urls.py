from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='edit'),
]
