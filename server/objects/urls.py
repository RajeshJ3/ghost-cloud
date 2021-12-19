from django.urls import path

from objects import views

urlpatterns = [
    path('', views.ObjectAPIView.as_view()),
]