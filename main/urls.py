
from django.urls import path  # path: Django's URL routing function (maps URLs to views)
from . import views           # .views: Imports view functions from current app's views.py

urlpatterns = [
    path('', views.home, name='home'),
    # - Maps to views.home function
    # - Named 'home' for template reverse URL lookups

    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    # - Dynamic URL capturing integer topic_id
    # - Routes to views.topic_detail view

    path('new-topic/', views.create_topic_with_entry, name='create_topic'),

]