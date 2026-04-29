from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_report, name='upload_report'),
    path('ask/', views.ask_question, name='ask_question'),
]