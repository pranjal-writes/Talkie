from django.urls import path
from. import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('usercheck', views.usercheck, name='usercheck'),
    path('logout/', views.logout, name='logout'),
]