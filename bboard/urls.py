from django.urls import path, include
# Импортируем созданное нами представление
from .views import *



urlpatterns = [
                path('', AdvList.as_view(), name='advlist'),
                path('adv/<int:pk>/', AdvView.as_view(), name='adv_detail'),
                path('adv/<int:pk>/edit/', AdvUpdate.as_view(), name='adv_edit'),
                path('adv/<int:pk>/delete/', AdvDelete.as_view(), name='adv_delete'),
                path('adv/create/', AdvCreate.as_view(), name='adv_create'),
                path('register/', RegisterUser.as_view(), name='register'),
                path('onetimecodeinput/', onetimecodeinput, name='onetimecodeinput'),
                path('activation/', activation, name='activation'),
                path('login/', LoginUser.as_view(), name='login'),
                path('logout/', logout_user, name='logout'),
                path('user_edit/', UserDataUpdate.as_view(), name='user_edit'),
                path('resp_add/<int:adv_id>/', ResponseCreate.as_view(), name='response_add'),
                path('user_response/', user_response, name='user_response'),
                path('response_delete/<int:pk>/', RespDelete.as_view(), name='response_delete'),
                path('response_accept/<int:resp_id>/', response_accept, name='response_accept'),
              ]
