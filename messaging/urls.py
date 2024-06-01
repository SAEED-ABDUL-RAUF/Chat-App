from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('group/<str:group_name>/', views.groupChatPage, name='group-page'),
    path('join/<int:pk>/', views.joinGroup, name='join-group'),
    path('groups/', views.groupList, name='groups-list'),
]