from django.urls import path, include
from rest_framework.routers import DefaultRouter

from profiles import views

router = DefaultRouter()
router.register('profiles', views.ProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('', include(router.urls)),
]
