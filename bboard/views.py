from random import SystemRandom

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from django_filters.views import FilterView

from .forms import *
from .models import *
from .filters import *
from django.conf import settings

paginator_items_count = 10

class AdvList(ListView):
    model = Adv
    ordering = '-date_create'
    template_name = 'bboard/advlist.html'
    context_object_name = 'advs'
    paginate_by = paginator_items_count

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['filterset'] = self.filterset
        context['cats'] = Category.objects.all()
        return context


class AdvView(DetailView):
    model = Adv
    template_name = 'bboard/adv.html'
    context_object_name = 'adv'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем все отклики к объявлению.
        context['resp'] = Response.objects.filter(adv_id=self.object)
        context['cats'] = Category.objects.all()
        return context


class RegisterUser(CreateView):
    form_class = BaseRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('activation')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        # создаем ключ
        new_random_obj = SystemRandom()
        onetime_key = EmailKey.objects.create(key=new_random_obj.randrange(100000, 999999), user_id=user)
        # отправляем письмо на почту
        send_mail(
            subject='Код для активации учетной записи (BulletinBoard)',
            message=f'Одноразовый код для активации учетной записи: {onetime_key.key}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'


class UserDataUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserDataForm
    model = User
    template_name = 'user/user_edit.html'
    success_url = reverse_lazy('advlist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование данных пользователя:'
        return context

    def get_object(self):
        return self.request.user


def logout_user(request):
    logout(request)
    return redirect('login')

def onetimecodeinput(request):
    if request.method == 'POST':
        username = request.POST['username']
        code = request.POST['code']
        if EmailKey.objects.filter(key=code, user_id__username=username):
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('login')
        else:
            return HttpResponse('Неверное имя пользователя и/или одноразовый код.')
    else:
        return render(request, 'user/activation.html')


def activation(request):
    return render(request, 'user/activation.html')


class AdvCreate(LoginRequiredMixin, CreateView):
    form_class = AdvForm
    model = Adv
    template_name = 'bboard/adv_edit.html'

    def form_valid(self, form):
        adv = form.save(commit=False)
        adv.user_id = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание объявления:'
        return context

    def get_success_url(self):
        return reverse('adv_detail', args=(self.object.id,))

class AdvUpdate(UpdateView):
    form_class = AdvForm
    model = Adv
    template_name = 'bboard/adv_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование объявления:'
        return context

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user_id != self.request.user:
            return HttpResponseForbidden()
        return super(AdvUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('adv_detail', args=(self.object.id,))


class AdvDelete(LoginRequiredMixin, DeleteView):
    model = Adv
    template_name = 'bboard/adv_delete.html'
    success_url = reverse_lazy('advlist')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user_id != self.request.user:
            return HttpResponseForbidden()
        return super(AdvDelete, self).dispatch(request, *args, **kwargs)


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'bboard/resp_edit.html'

    def form_valid(self, form):
        resp = form.save(commit=False)
        resp.user_id = self.request.user
        adv = Adv.objects.get(pk=self.kwargs['adv_id'])
        resp.adv_id = adv
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление отклика:'
        return context

    def get_success_url(self):
        return reverse('adv_detail', args=(self.object.adv_id.pk,))

class PostList(ListView):
    model = Response
    ordering = '-date_create'
    template_name = 'bboard/resplist.html'
    context_object_name = 'resp'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RespFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def user_response(request):
    u = request.user
    queryset = Response.objects.filter(adv_id__in=u.adv_set.all())
    filterset = RespFilter(request.GET, my_user_id=u.pk, queryset=queryset)
    context = {
        'resp': filterset.qs,
        'filterset': filterset,
    }
    return render(request, 'bboard/search.html', context=context)


class RespDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'bboard/resp_delete.html'
    success_url = reverse_lazy('user_response')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.adv_id.user_id != self.request.user:
            return HttpResponseForbidden()
        return super(RespDelete, self).dispatch(request, *args, **kwargs)


@login_required
def response_accept(request, resp_id):
    resp = Response.objects.get(pk=resp_id)
    user = User.objects.get(pk=resp.user_id.pk)
    # отправляем письмо на почту
    send_mail(
        subject='Ваш отклик принят.',
        message=f'Пользователь {request.user} принял ваш отклик!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return HttpResponse('Подтверждение принятия отклика - письмо пользователю, оставившему отклик, отправлено!')
