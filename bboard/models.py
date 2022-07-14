from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name_category = models.CharField(max_length=100)  # наименование категории

    def __str__(self):
        return self.name_category

class Adv(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)  # дата и время создания объявления
    header = models.CharField(max_length=255)  # заголовок объявления
    text = RichTextUploadingField(blank=True, null=True)  # текст объявления
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # автор объявления
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)  # категория объявления (по тех заданию - одна для объявления)

    def preview(self):  # предварительный просмотр объявления
        return self.text[:124] + '...'

    def __str__(self):
        return self.header

    # def get_absolute_url(self):
    #     return reverse('news_detail', args=[str(self.id)])


class Response(models.Model):
    text = models.TextField(max_length=1000)     # текст отклика
    date_create = models.DateTimeField(auto_now_add=True)  # дата и время создания отклика
    adv_id = models.ForeignKey(Adv, on_delete=models.CASCADE)   # объявление, к которому был отклик
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)     # пользователь оставивший отклик

    def __str__(self):
        return self.text[:124]

class EmailKey(models.Model):
    key = models.CharField(max_length=6)    # одноразовый код
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)     # кому послан код
    dt_sended = models.DateTimeField(auto_now_add=True)    # дата/время отправки кода (можно использовать для удаления)