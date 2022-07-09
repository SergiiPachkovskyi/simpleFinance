from django.test import SimpleTestCase
from django.urls import reverse, resolve
from fin.views import index, user_login, user_registration, user_logout, Articles, EditArticle, AddArticle,\
    RemoveArticle, article_delete_error, CashFlows, AddCashFlow, RemoveCashFlow, cash_flow_delete_error, article_graph


class TestUrls(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, index)

    def test_registration_url_resolves(self):
        url = reverse('registration')
        self.assertEqual(resolve(url).func, user_registration)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, user_login)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, user_logout)

    def test_articles_url_resolves(self):
        url = reverse('articles')
        self.assertEqual(resolve(url).func.view_class, Articles)

    def test_edit_article_url_resolves(self):
        url = reverse('edit_article', args=[1])
        self.assertEqual(resolve(url).func.view_class, EditArticle)

    def test_add_article_url_resolves(self):
        url = reverse('add_article')
        self.assertEqual(resolve(url).func.view_class, AddArticle)

    def test_remove_article_url_resolves(self):
        url = reverse('remove_article', args=[1])
        self.assertEqual(resolve(url).func.view_class, RemoveArticle)

    def test_article_delete_error_url_resolves(self):
        url = reverse('article_delete_error')
        self.assertEqual(resolve(url).func, article_delete_error)

    def test_cash_flows_url_resolves(self):
        url = reverse('cash_flows')
        self.assertEqual(resolve(url).func.view_class, CashFlows)

    def test_add_cash_flow_url_resolves(self):
        url = reverse('add_cash_flow')
        self.assertEqual(resolve(url).func.view_class, AddCashFlow)

    def test_remove_cash_flow_url_resolves(self):
        url = reverse('remove_cash_flow', args=[1])
        self.assertEqual(resolve(url).func.view_class, RemoveCashFlow)

    def test_cash_flow_delete_error_url_resolves(self):
        url = reverse('cash_flow_delete_error')
        self.assertEqual(resolve(url).func, cash_flow_delete_error)

    def test_article_graph_url_resolves(self):
        url = reverse('article_graph', args=[1])
        self.assertEqual(resolve(url).func, article_graph)
