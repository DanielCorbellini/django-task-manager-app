from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.page.as_view(), name='Login')
]
