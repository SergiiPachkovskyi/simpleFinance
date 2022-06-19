from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth import login, logout

from .forms import ArticleForm, CashFlowForm
from .models import Article, CashFlow


def index(request, current_year=None, current_month=None):
    context = dict()
    if request.user.is_authenticated:
        articles = Article.objects.filter(user_id=request.user.id)
        cash_flows = CashFlow.objects.filter(article__user_id=request.user.id).select_related('article')
        # distinct('item_name') not working with MySql
        # months = set()
        # for cf in cash_flows:
        #     months.add(cf.fin_month)
        cf_months = CashFlow.objects.filter(article__user_id=request.user.id).distinct('fin_month')
        months = [m.fin_month for m in cf_months]
        str_month = '...'
        if current_month is None:
            if len(months) != 0:
                current_year = months[0].year
                month = months[0].month
                current_month = month
                str_month = str(month) if len(str(month)) == 2 else ("0" + str(month))
        else:
            str_month = str(current_month) if len(str(current_month)) == 2 else ("0" + str(current_month))

        context = {
            'articles':  articles,
            'cash_flows': cash_flows,
            'months': months,
            'current_year': current_year,
            'current_month': current_month,
            'str_month': str_month,
        }
    return render(request, template_name='fin/index.html', context=context)


def user_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'fin/registration.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'fin/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('home')


class Articles(ListView):
    model = Article
    template_name = 'fin/articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(user_id=self.request.user.id)


class AddArticle(CreateView):
    form_class = ArticleForm
    template_name = 'fin/add_article.html'

    def get_form_kwargs(self):
        kwargs = super(AddArticle, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class RemoveArticle(DeleteView):
    model = Article
    success_url = reverse_lazy('articles')
    error_url = reverse_lazy('article_delete_error')

    def get_error_url(self):
        if self.error_url:
            return self.error_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No error URL to redirect to. Provide a error_url.")

    def get_success_url(self):
        if self.error_url:
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No success URL to redirect to. Provide a success_url.")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        error_url = self.get_error_url()

        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except models.ProtectedError:
            return HttpResponseRedirect(error_url)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


def article_delete_error(request):
    return render(request, template_name='fin/article_delete_error.html')


class CashFlows(ListView):
    model = CashFlow
    template_name = 'fin/cash_flows.html'
    context_object_name = 'cash_flows'

    def get_queryset(self):
        return CashFlow.objects.filter(article__user_id=self.request.user.id)


class AddCashFlow(CreateView):
    form_class = CashFlowForm
    template_name = 'fin/add_cash_flow.html'

    def get_queryset(self):
        return CashFlow.objects.filter(article__user_id=self.request.user.id)

    def get_form_kwargs(self):
        kwargs = super(AddCashFlow, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class RemoveCashFlow(DeleteView):
    model = CashFlow
    success_url = reverse_lazy('cash_flows')
    error_url = reverse_lazy('cash_flow_delete_error')

    def get_error_url(self):
        if self.error_url:
            return self.error_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No error URL to redirect to. Provide a error_url.")

    def get_success_url(self):
        if self.error_url:
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No success URL to redirect to. Provide a success_url.")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        error_url = self.get_error_url()

        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except models.ProtectedError:
            return HttpResponseRedirect(error_url)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


def cash_flow_delete_error(request):
    return render(request, template_name='fin/article_delete_error.html')



