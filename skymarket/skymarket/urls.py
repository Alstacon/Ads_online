from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from djoser.views import UserViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads.views import AdViewSet, CommentViewSet


users_router = SimpleRouter()

users_router.register('api/users', UserViewSet, basename='users')

router = SimpleRouter()

router.register('api/ads', AdViewSet, basename='ads')

comments_router = NestedSimpleRouter(
    router,
    'api/ads',
    lookup='ad'
)

comments_router.register('comments', CommentViewSet, basename='ad_comments')

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/redoc-tasks/", include("redoc.urls")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/shema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),

    path('', include(users_router.urls)),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view())

]

urlpatterns += router.urls
urlpatterns += comments_router.urls
urlpatterns += users_router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
