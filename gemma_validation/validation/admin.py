"""
Admin configuration for validation models
"""
from django.contrib import admin
from .models import JapaneseExercise, GemmaValidationResult, TestSession


@admin.register(JapaneseExercise)
class JapaneseExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'exercise_type', 'jlpt_level', 'created_at')
    list_filter = ('exercise_type', 'jlpt_level', 'created_at')
    search_fields = ('title', 'prompt')


@admin.register(GemmaValidationResult)
class GemmaValidationResultAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'model_name', 'status', 'is_correct', 'confidence_score', 'created_at')
    list_filter = ('status', 'is_correct', 'model_name', 'provider')
    search_fields = ('exercise__title', 'gemma_response')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_name', 'total_tests', 'passed_tests', 'success_rate', 'created_at')
    list_filter = ('model_name', 'provider', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
