from django.urls import path, include
from . import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('user-profile/<str:username>/', views.UserProfileDetailView.as_view(), name='profile-detail'),
    path('', include('allauth.urls')),
]