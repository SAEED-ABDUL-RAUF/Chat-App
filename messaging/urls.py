from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('group/<str:group_name>/', views.groupView, name='group'),
]