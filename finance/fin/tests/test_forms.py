from django.contrib.auth.models import User
from django.test import TestCase
from fin.forms import UserRegisterForm, UserLoginForm, ArticleForm, CashFlowForm
from fin.models import Article


class TestForms(TestCase):
    def setUp(self):
        self.user = User()
        self.user.username = 'user2'
        self.user.password = 'poiLJK789'
        self.user.save()

        self.article = Article()
        self.article.title = 'test'
        self.article.user = self.user
        self.article.save()

        self.client.login(username=self.user.username, password='Asdqwe123')

    def test_user_exist(self):
        count = User.objects.all().count()
        self.assertEquals(count, 1)

    def test_user_register_form_data(self):
        form = UserRegisterForm(data={
            'username': 'user1',
            'password1': 'Asdqwe123!',
            'password2': 'Asdqwe123!',
            'email': 'user@gmail.com',
        })
        self.assertTrue(form.is_valid())

    def test_user_register_form_no_data(self):
        form = UserRegisterForm(data={
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    # def test_user_login_form_data(self):
    #     form = UserLoginForm(data={
    #         'username': self.user.username,
    #         'password': self.user.password,
    #     })
    #     print(form.errors)
    #     self.assertTrue(form.is_valid())

    def test_user_login_form_no_data(self):
        form = UserLoginForm(data={
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_article_form_data(self):
        form = ArticleForm(data={
            'title': 'article1',
            'photo': 'finance/static/finance/images/article.png',
        })
        self.assertTrue(form.is_valid())

    def test_article_form_no_data(self):
        form = ArticleForm(data={
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    # def test_cash_flow_form_data(self):
    #     form = CashFlowForm(data={
    #         'fin_month': '01.01.2022',
    #         'is_profit': 'True',
    #         'sum': '123',
    #         'article': self.article.pk,
    #     })
    #     print(form.errors)
    #     self.assertTrue(form.is_valid())

    def test_cash_flow_form_no_data(self):
        form = CashFlowForm(data={
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)
