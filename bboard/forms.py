from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import *


class BaseRegisterForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    email = forms.EmailField(label="Адрес e-mail")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2",)


class UserDataForm(UserChangeForm):
    username = forms.CharField(label='Имя пользователя / Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email')


class AdvForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdvForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Adv
        fields = ['header', 'text', 'categories']
        labels = {
            'header': 'Заголовок объявления',
            'text': 'Текст объявления',
            'categories': 'Категории',
        }


class ResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Response
        fields = ['text']
        labels = {
            'text': 'Текст отклика',
        }
