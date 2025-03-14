from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings

from schema_graph.views import Schema

# admin.site.register(UploadImage)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('api/', include("authentication.urls")),
    path('api/', include('files.urls')),
    path("schema/", Schema.as_view())
    # re_path('signup', include("authentication.urls.signup")),
    # re_path('test_token', include("authentication.urls.test_token")),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
