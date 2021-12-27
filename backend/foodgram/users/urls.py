from django.urls import include, path
from rest_framework.routers import (
    DefaultRouter, DynamicRoute, Route, SimpleRouter
)

from .views import UserViewSet, SubscriptionsViewSet, SubscribeViewSet


class SubscribeRouter(SimpleRouter):

    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{lookup}/{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        DynamicRoute(
            url=r'^{lookup}/{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]


router = DefaultRouter()
router.register(
    'subscriptions', SubscriptionsViewSet, basename='subscriptions'
)
router.register('', UserViewSet, basename='users')


subscribe_router = SubscribeRouter()
subscribe_router.register(
    r'(?P<id>\d+)/subscribe', SubscribeViewSet, basename='subscribe'
)


urlpatterns = [
    path('', include(subscribe_router.urls))
]

#urlpatterns += router.urls
