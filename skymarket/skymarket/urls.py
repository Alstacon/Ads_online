from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from djoser.views import UserViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

users_router = SimpleRouter()

users_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/redoc-tasks/", include("redoc.urls")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/shema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),

    path('', include(users_router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
