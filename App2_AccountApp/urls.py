from django.urls import path
from . import views

app_name = 'App2_AccountApp'

urlpatterns = [
    path('home/profile_view/', views.profile_view, name='profile'),
    path('<username>/', views.profile_view, name='userprofile'),
    
    path('profile/profile_edit/', views.profile_edit, name='profile-edit'),
    path('profile/delete_account/', views.delete_account, name='delete-account'),
]