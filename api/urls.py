from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('projects/', views.ProjectListAPIView.as_view(), name="project-list"),
    path('projects/<slug:slug>/', views.ProjectDetailAPIView.as_view(), name="project-details"),
    path('playground/echo/', views.EchoPlaygroundAPIView.as_view(), name='playground-echo'),
]
