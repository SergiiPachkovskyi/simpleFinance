from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Article, CashFlow


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    sortable_by = ('id', 'title', 'user')
    readonly_fields = ('get_photo',)
    fields = ('title', 'user', 'photo', 'get_photo')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return "-"

    get_photo.short_description = 'Мініатюра'


class CashFlowAdmin(admin.ModelAdmin):
    list_display = ('id', 'fin_month', 'article', 'is_profit', 'sum')
    list_display_links = ('id', 'fin_month', 'article')
    search_fields = ('fin_month',)
    sortable_by = ('id', 'fin_month', 'article')
    fields = ('fin_month', 'article', 'is_profit', 'sum')


admin.site.register(Article, ArticleAdmin)
admin.site.register(CashFlow, CashFlowAdmin)
