from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
# swage u-n
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
# translate u-n
from django.conf.urls.i18n import i18n_patterns
# debug
from django.views.static import serve

# swagger u-n
schema_view = get_schema_view(
    openapi.Info(
        title="Instagram clone API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('userapp.urls')),
    path('', include('blogapp.urls')),
    #     swager u-n
    re_path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # debug
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

# translate u-n
urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
