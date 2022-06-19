# Generated by Django 4.0.5 on 2022-06-09 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Url')),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d', verbose_name='Зображення')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Стаття(ю)',
                'verbose_name_plural': 'Статті',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='CashFlow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_month', models.DateTimeField()),
                ('is_profit', models.BooleanField(default=False, verbose_name='Прибуток')),
                ('sum', models.FloatField()),
                ('comment', models.CharField(max_length=250)),
                ('user_article_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fin.article', verbose_name='Стаття')),
            ],
            options={
                'verbose_name': 'Рух коштів',
                'verbose_name_plural': 'Рух коштів',
                'ordering': ['-fin_month'],
            },
        ),
    ]
