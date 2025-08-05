from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('create_topic/', views.create_topic_with_entry, name='create_topic'),
    path('register/', views.register, name='register'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('search/', views.search, name='search'),
]
