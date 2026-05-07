"""
URL Configuration for gemma_validation
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from validation.views import ExerciseViewSet, ValidationResultViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'results', ValidationResultViewSet, basename='result')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/validate/', include('validation.urls')),
]
