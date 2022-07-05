from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from fin.models import Article, CashFlow


class UserLoginForm(AuthenticationForm):
    """A class to represent a Login form."""
    username = forms.CharField(label="Ім'я користувача", widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserRegisterForm(UserCreationForm):
    """A class to represent a Register form."""
    username = forms.CharField(label="Ім'я користувача", widget=forms.TextInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Підтвердження пароля",
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ArticleForm(forms.ModelForm):
    """A class to represent an Articles form."""
    title = forms.CharField(label="Заголовок", widget=forms.TextInput(attrs={'class': "form-control"}))
    photo = forms.ImageField(label="Зображення", widget=forms.FileInput(attrs={'class': "form-control"}))

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
    """A class to represent a CashFlows form."""
    fin_month = forms.DateField(label="Дата", widget=forms.DateInput(attrs={'class': "form-control"}))
    sum = forms.FloatField(label="Сума", widget=forms.NumberInput(attrs={'class': "form-control"}))
    article = forms.ModelChoiceField(label="Стаття", empty_label='Оберіть статтю...', queryset=None,
                                     widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CashFlowForm, self).__init__(*args, **kwargs)
        self.fields["article"].queryset = Article.objects.filter(user=user)

    class Meta:
        model = CashFlow
        fields = ['fin_month', 'article', 'is_profit', 'sum']
