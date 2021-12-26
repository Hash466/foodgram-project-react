from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SubscriptionsViewSet

router = DefaultRouter()
router.register('subscriptions/', SubscriptionsViewSet, basename='users')
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
