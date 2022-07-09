from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from fin.models import Article, CashFlow


class TestView(TestCase):
    def setUp(self):
        self.user = User()
        self.user.username = 'default_user'
        self.user.password = 'poiLJK789'
        self.user.email = 'user@gmail.com'
        self.user.save()

        self.article = Article()
        self.article.title = 'test'
        self.article.user = self.user
        self.article.save()

        self.cf = CashFlow()
        self.cf.fin_month = datetime.now()
        self.cf.article = self.article
        self.cf.sum = 123
        self.cf.is_profit = True
        self.cf.save()

        # self.client = Client()
        # self.client.login(username='default_user', password='poiLJK789')

    def test_index(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fin/index.html')

    def test_index_with_params(self):
        url = reverse('home', args=[2022, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fin/index.html')

    def test_user_registration_GET(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fin/registration.html')

    def test_user_registration_POST(self):
        response = self.client.post(reverse('registration'), {
            'username': 'user1',
            'password1': 'poiLJK789',
            'password2': 'poiLJK789',
            'email': 'user@gmail.com',
        }, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_user_login_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fin/login.html')

    def test_user_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_articles(self):
        url = reverse('articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fin/articles.html')

    def test_add_articles_GET(self):
        url = reverse('add_article')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fin/add_article.html')

    # def test_add_articles_POST(self):
    #     url = reverse('add_article')
    #     response = self.client.post(url, {
    #         'title': 'art1',
    #         'user': self.user.pk,
    #     }, format='text/html')
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'fin/articles.html')

    def test_edit_articles_GET(self):
        url = reverse('edit_article', args=[self.article.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fin/edit_article.html')

    def test_cash_flows(self):
        url = reverse('cash_flows')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fin/cash_flows.html')

    def test_article_graph(self):
        url = reverse('article_graph', args=[self.article.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fin/article_graph.html')

