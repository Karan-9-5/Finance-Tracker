from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import Transaction, Category, Budget
from .forms import TransactionForm, BudgetForm
import datetime
from django.utils import timezone

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Totals
        transactions = Transaction.objects.filter(user=user)
        total_income = transactions.filter(category__type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(category__type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
        savings = total_income - total_expense
        
        context['total_income'] = total_income
        context['total_expense'] = total_expense
        context['savings'] = savings
        
        # Recent Transactions
        context['recent_transactions'] = transactions.order_by('-date')[:5]
        
        return context

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date')

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'finance/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'finance/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'finance/budget_form.html'
    success_url = reverse_lazy('budget_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MonthlyReportView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/monthly_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get data for the last 6 months
        report_data = []
        today = datetime.date.today()
        for i in range(6):
            month_date = today - datetime.timedelta(days=i*30)
            month = month_date.month
            year = month_date.year
            
            transactions = Transaction.objects.filter(user=user, date__month=month, date__year=year)
            income = transactions.filter(category__type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
            expense = transactions.filter(category__type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
            
            report_data.append({
                'month': month_date.strftime('%B %Y'),
                'income': income,
                'expense': expense,
                'savings': income - expense
            })
            
        context['report_data'] = report_data
        return context
