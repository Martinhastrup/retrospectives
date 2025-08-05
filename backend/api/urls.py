from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'retrospectives', views.RetrospectiveViewSet)
router.register(r'retrospective-items', views.RetrospectiveItemViewSet)
router.register(r'action-items', views.ActionItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 