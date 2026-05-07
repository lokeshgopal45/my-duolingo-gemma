"""
Serializers for validation API
"""
from rest_framework import serializers
from .models import JapaneseExercise, GemmaValidationResult, TestSession


class JapaneseExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = JapaneseExercise
        fields = ['id', 'title', 'exercise_type', 'jlpt_level', 'prompt', 
                  'context', 'correct_answers', 'explanation', 'created_at']
        read_only_fields = ['created_at']


class GemmaValidationResultSerializer(serializers.ModelSerializer):
    exercise_title = serializers.CharField(source='exercise.title', read_only=True)
    
    class Meta:
        model = GemmaValidationResult
        fields = ['id', 'exercise', 'exercise_title', 'model_name', 'provider',
                  'prompt_sent', 'gemma_response', 'status', 'is_correct',
                  'confidence_score', 'validation_notes', 'response_time_ms',
                  'token_count', 'created_at']
        read_only_fields = ['created_at', 'gemma_response', 'response_time_ms', 'token_count']


class TestSessionSerializer(serializers.ModelSerializer):
    success_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = TestSession
        fields = ['id', 'name', 'description', 'model_name', 'provider',
                  'config', 'total_tests', 'passed_tests', 'success_rate',
                  'created_at']
        read_only_fields = ['created_at', 'total_tests', 'passed_tests']
    
    def get_success_rate(self, obj):
        return obj.success_rate
