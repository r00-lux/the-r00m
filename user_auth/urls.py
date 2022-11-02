from django.urls import path
from user_auth import views

app_name = "user_auth"

urlpatterns = [path('token/', views.CreateTokenView.as_view(), name='token')]
