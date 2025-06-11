from django.contrib import admin
from django.urls import path,include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns

# import jazzmin
schema_view = get_schema_view(
    openapi.Info(
        title="booking API",
        default_version="v1",
        description="API documentation for the booking project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="booking@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # For language switching endpoint
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),

    path('api/auth/', include('rest_framework.urls')),
    path('api/book/', include('book.urls')),
    # path('api/users/', include('users.urls')),

    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)