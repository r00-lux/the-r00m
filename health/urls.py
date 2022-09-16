from django.urls import path
from health import views

app_name = "health"

urlpatterns = [path('', views.HealthView.as_view(), name='health')]
