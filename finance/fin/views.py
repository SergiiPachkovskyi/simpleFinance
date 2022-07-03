import collections
import json
from calendar import monthrange
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth import login, logout

from .forms import ArticleForm, CashFlowForm, UserLoginForm, UserRegisterForm
from .models import Article, CashFlow


def index(request, current_year: Optional[int] = None, current_month: Optional[int] = None):
    """
    Function for render index.html
    :param request: WSGIRequest
    :param current_year: int | None
    :param current_month: int | None
    :return: render fin/index.html
    """
    context = dict()
    print(type(request))
    if request.user.is_authenticated:
        articles = Article.objects.filter(user_id=request.user.id)
        cf_months = CashFlow.objects.filter(article__user_id=request.user.id).distinct('fin_month')
        years = [m.fin_month.year for m in cf_months]
        years = sorted(set(years), reverse=True)
        months = [m.fin_month.replace(day=1) for m in cf_months]
        months = sorted(set(months), reverse=True)

        if current_month is None and current_year is None:
            if len(months) != 0:
                current_year = months[0].year
                month = months[0].month
                current_month = month
            else:
                current_year = datetime.now().year
                current_month = datetime.now().month

        str_month = str(current_month) if len(str(current_month)) == 2 else ("0" + str(current_month))
        start_date = datetime.strptime(str(current_year) + '-' + str_month + '-01', '%Y-%m-%d')
        end_date = datetime.strptime(str(current_year) + '-' + str_month + '-'
                                     + str(monthrange(start_date.year, start_date.month)[1]), '%Y-%m-%d')
        cash_flows = CashFlow.objects.filter(article__user_id=request.user.id,
                                             fin_month__range=(start_date, end_date)). \
            order_by('fin_month').select_related('article')

        context = {
            'articles': articles,
            'cash_flows': cash_flows,
            'months': months,
            'years': years,
            'current_year': current_year,
            'current_month': current_month,
            'str_month': str_month,
        }
    return render(request, template_name='fin/index.html', context=context)


def user_registration(request):
    """
    Function for render registration.html
    :param request: WSGIRequest
    :return: render fin/registration.html
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вдала реєстрація')
            return redirect('home')
        else:
            messages.error(request, 'Помилка реєстрації')
    else:
        form = UserRegisterForm()
    return render(request, 'fin/registration.html', {"form": form})


def user_login(request):
    """
    Function for render login.html
    :param request: WSGIRequest
    :return: render fin/login.html
    """
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Помилка авторизації')
    else:
        form = UserLoginForm()
    return render(request, 'fin/login.html', {"form": form})


def user_logout(request):
    """
    Function for render login.html
    :param request: WSGIRequest
    :return: redirect('home')
    """
    logout(request)
    return redirect('home')


class Articles(ListView):
    """
    Display a list of Articles.
    :model:`Article`
    :context_object_name:`articles`
    :template_name:`fin/articles.html`
    """
    model = Article
    template_name = 'fin/articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(user_id=self.request.user.id)


class EditArticle(UpdateView):
    """
    Display an Article edit page.
    :model:`Article`
    :context_object_name:`article`
    :fields: 'title', 'photo'
    :template_name:`fin/edit_article.html`
    """
    model = Article
    template_name = 'fin/edit_article.html'
    fields = ['title', 'photo']
    context_object_name = 'article'


class AddArticle(CreateView):
    """
    Display an ArticleForm
    :form_class:`ArticleForm`
    :template_name:`fin/edit_article.html`
    """
    form_class = ArticleForm
    template_name = 'fin/add_article.html'

    def get_form_kwargs(self):
        kwargs = super(AddArticle, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class RemoveArticle(DeleteView):
    """
    Display an Article remove page.
    :model:`Article`
    :success_url:`articles`
    :error_url: `article_delete_error`
    """
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
    """
    Function for render article_delete_error.html
    :param request: WSGIRequest
    :return: render fin/article_delete_error.html
    """
    return render(request, template_name='fin/article_delete_error.html')


class CashFlows(ListView):
    """
    Display a list of CashFlows.
    :model:`Article`
    :context_object_name:`cash_flows`
    :template_name:`fin/cash_flows.html`
    """
    model = CashFlow
    template_name = 'fin/cash_flows.html'
    context_object_name = 'cash_flows'

    def get_queryset(self):
        date = self.request.GET.get('d')
        if date is None:
            return CashFlow.objects.filter(article__user_id=self.request.user.id)
        else:
            start_date = datetime.strptime(date + '-01', '%Y-%m-%d')
            end_date = datetime.strptime(date + '-' + str(monthrange(start_date.year, start_date.month)[1]), '%Y-%m-%d')
            return CashFlow.objects.filter(article__user_id=self.request.user.id,
                                           fin_month__range=(start_date, end_date))

    def get_context_data(self, **kwargs):
        context = super(CashFlows, self).get_context_data(**kwargs)
        date = self.request.GET.get('d')
        if date is None:
            current_date = datetime.now()
            context['str_year'] = current_date.year
            month = current_date.month
            context['str_month'] = str(month) if len(str(month)) == 2 else ("0" + str(month))
        else:
            current_date = datetime.strptime(date + '-01', '%Y-%m-%d')
            context['current_date'] = current_date
            context['str_year'] = current_date.year
            month = current_date.month
            context['str_month'] = str(month) if len(str(month)) == 2 else ("0" + str(month))
        return context


class AddCashFlow(CreateView):
    """
    Display an CashFlowForm
    :form_class:`CashFlowForm`
    :template_name:`fin/add_cash_flow.html`
    """
    form_class = CashFlowForm
    template_name = 'fin/add_cash_flow.html'

    def get_form_kwargs(self):
        kwargs = super(AddCashFlow, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class RemoveCashFlow(DeleteView):
    """
    Display an CashFlow remove page.
    :model:`CashFlow`
    :success_url:`cash_flows`
    :error_url: `cash_flow_delete_error`
    """
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
    """
    Function for render article_delete_error.html
    :param request: WSGIRequest
    :return: render fin/article_delete_error.html
    """
    return render(request, template_name='fin/article_delete_error.html')


def article_graph(request, pk: int):
    """
    Function for render article_graph.html
    :param request: WSGIRequest
    :param pk: int
    :return: render fin/article_graph.html
    """
    context = dict()
    if request.user.is_authenticated:
        article = Article.objects.get(pk=pk)

        cash_flows = CashFlow.objects.filter(article=article).distinct('fin_month').order_by('fin_month')

        context = {
            'article': article,
        }

        if len(cash_flows) != 0:
            months = dict()
            min_month = None
            max_month = None
            for cf in cash_flows:
                month = cf.fin_month.replace(day=1)
                if min_month is None:
                    min_month = cf.fin_month
                max_month = month
                sum = cf.sum if cf.is_profit else -cf.sum
                months[month] = months[month] + sum if month in months else sum

            current_month = min_month + relativedelta(months=1)
            while current_month < max_month:
                if current_month in months:
                    pass
                else:
                    months[current_month] = 0
                current_month = current_month + relativedelta(months=1)

            months = collections.OrderedDict(sorted(months.items()))
            month_list = list(months.keys())
            sum_list = list(months.values())

            charts_data = dict()
            charts_data["article"] = article.title
            charts_data["charts_articles"] = dict()
            charts_data["charts_articles"]["month_list"] = month_list
            charts_data["charts_articles"]["sum_list"] = [
                {"name": article.title, "data": sum_list},
            ]

            def custom_serializer(obj):
                if isinstance(obj, date):
                    serial = obj.isoformat()
                    return serial
                elif isinstance(obj, Decimal):
                    return float(obj)

            charts_data = json.dumps(charts_data, default=custom_serializer)
            context['charts_data'] = charts_data

    return render(request, template_name='fin/article_graph.html', context=context)
