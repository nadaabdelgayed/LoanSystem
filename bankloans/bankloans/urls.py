from django.contrib import admin
from django.urls import path, include
from loans import urls as loans_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(loans_urls)),
]
