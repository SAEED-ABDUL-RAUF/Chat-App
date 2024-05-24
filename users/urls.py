from django.urls import path, include


urlpatterns = [
    # path('register/', user_views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    # path('profile/', user_views.profile, name='profile'),
]