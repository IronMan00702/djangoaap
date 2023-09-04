from django.urls import path
from . import views

urlpatterns = [
    path('', views.members, name='members'),
    path('upload/', views.upload_file, name='upload_file'),
    path('ask/', views.ask_question, name='ask_question'),
]