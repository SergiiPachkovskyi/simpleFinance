from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Користувач')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Зображення', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("articles")

    class Meta:
        verbose_name = 'Стаття(ю)'
        verbose_name_plural = 'Статті'
        ordering = ['title']


class CashFlow(models.Model):
    fin_month = models.DateField(verbose_name='Місяць')
    article = models.ForeignKey(Article, on_delete=models.PROTECT, verbose_name='Стаття')
    is_profit = models.BooleanField(default=False, verbose_name='Прибуток')
    sum = models.FloatField(verbose_name='Сума')
    comment = models.CharField(max_length=250, blank=True, verbose_name='Коментар')

    def __str__(self):
        return str(self.fin_month) + ' ' + str(self.article)

    def get_absolute_url(self):
        return reverse("cash_flows")

    class Meta:
        verbose_name = 'Рух коштів'
        verbose_name_plural = 'Рух коштів'
        ordering = ['-fin_month', 'article']
