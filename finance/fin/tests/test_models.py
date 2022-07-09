from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from fin.models import Article, CashFlow


class ArticleModelTest(TestCase):

    def setUp(self):
        self.user = User()
        self.user.username = 'user'
        self.user.password = 'user'
        self.user.save()

        self.article = Article()
        self.article.title = 'test'
        self.article.user = self.user
        self.article.save()

    def test_fields(self):
        article = Article()
        article.title = 'test'
        article.user = User.objects.get(pk=self.user.pk)
        article.save()

        record = Article.objects.get(pk=article.pk)
        self.assertEqual(record, article)

    def test_get_absolute_url(self):
        self.assertEqual("/articles/", self.article.get_absolute_url())


class CashFlowModelTest(TestCase):

    def setUp(self):
        user = User()
        user.username = 'user'
        user.password = 'user'
        user.save()

        self.article = Article()
        self.article.title = 'test'
        self.article.user = user
        self.article.save()

        self.cf = CashFlow()
        self.cf.fin_month = datetime.now()
        self.cf.is_profit = True
        self.cf.sum = 123
        self.cf.comment = 'comment'
        self.cf.article = self.article
        self.cf.save()

    def test_fields(self):
        cf = CashFlow()
        cf.fin_month = datetime.now()
        cf.is_profit = True
        cf.sum = 123
        cf.comment = 'comment'
        cf.article = self.article
        cf.save()

        record = CashFlow.objects.get(pk=cf.pk)
        self.assertEqual(record, cf)

    def test_get_absolute_url(self):
        self.assertEqual("/cash_flows/", self.cf.get_absolute_url())
