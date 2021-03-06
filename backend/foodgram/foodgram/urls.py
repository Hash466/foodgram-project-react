from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('recipe.urls')),
    path('api/', include('users.urls')),
]
