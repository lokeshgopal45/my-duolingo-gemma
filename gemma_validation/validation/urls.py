"""
URL Configuration for validation API
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet, ValidationResultViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'results', ValidationResultViewSet, basename='result')

urlpatterns = router.urls
