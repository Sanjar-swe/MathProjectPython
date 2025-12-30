from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.views import QuestionViewSet, BotUserViewSet, TestAttemptViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'users', BotUserViewSet)
router.register(r'attempts', TestAttemptViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
