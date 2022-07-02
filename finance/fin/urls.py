from django.urls import path

from fin.views import *

urlpatterns = [
    path('', index, name='home'),
    path('<int:current_year>/<int:current_month>', index, name='home'),
    path('registration/', user_registration, name='registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('articles/', Articles.as_view(), name='articles'),
    path('articles/<int:pk>/edit', EditArticle.as_view(), name='edit_article'),
    path('add_article/', AddArticle.as_view(), name='add_article'),
    path('remove_article/<int:pk>', RemoveArticle.as_view(), name='remove_article'),
    path('article_delete_error', article_delete_error, name='article_delete_error'),

    path('cash_flows/', CashFlows.as_view(), name='cash_flows'),
    path('add_cash_flow/', AddCashFlow.as_view(), name='add_cash_flow'),
    path('remove_cash_flow/<int:pk>', RemoveCashFlow.as_view(), name='remove_cash_flow'),
    path('cash_flow_delete_error', cash_flow_delete_error, name='cash_flow_delete_error'),

    path('articles/<int:pk>/graph', article_graph, name='article_graph'),
]
