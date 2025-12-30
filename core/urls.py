from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.views import QuestionViewSet, BotUserViewSet, TestAttemptViewSet

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'users', BotUserViewSet)
router.register(r'attempts', TestAttemptViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # Swagger UI:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
