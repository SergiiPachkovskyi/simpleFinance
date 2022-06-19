from django import forms

from fin.models import Article, CashFlow


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user', None)
        super(ArticleForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        art = super().save(commit=False)
        art.user = self.current_user
        if commit:
            art.save()
            self.save_m2m()
        return art

    class Meta:
        model = Article
        fields = ['title', 'photo']


class CashFlowForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CashFlowForm, self).__init__(*args, **kwargs)
        self.fields["article"].queryset = Article.objects.filter(user=user)

    class Meta:
        model = CashFlow
        fields = ['fin_month', 'article', 'is_profit', 'sum']

