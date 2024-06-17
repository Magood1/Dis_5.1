from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet

router = DefaultRouter()
router.register(r'', AuthViewSet, basename='')

urlpatterns = [
    path('', include(router.urls)),
]

