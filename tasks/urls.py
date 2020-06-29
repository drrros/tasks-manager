from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_task/', views.create_task, name='create_task'),
    path('update_task/<str:pk>/', views.update_task, name='update_task'),
    path('delete_task/<str:pk>/', views.delete_task, name='delete_task'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user')
]
