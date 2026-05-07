"""
Validation app models for Gemma Japanese N3 exercise testing
"""
from django.db import models
import json

class JapaneseExercise(models.Model):
    """Japanese N3 exercise model"""
    EXERCISE_TYPES = [
        ('reading', 'Reading Comprehension'),
        ('grammar', 'Grammar'),
        ('vocabulary', 'Vocabulary'),
        ('listening', 'Listening'),
        ('kanji', 'Kanji'),
    ]
    
    title = models.CharField(max_length=255)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPES)
    jlpt_level = models.CharField(max_length=10, default='N3')
    
    # Exercise content (Japanese)
    prompt = models.TextField()
    context = models.TextField(blank=True, help_text="Background context if needed")
    
    # Expected answer(s)
    correct_answers = models.JSONField(default=list, help_text="List of acceptable answers")
    explanation = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.exercise_type})"


class GemmaValidationResult(models.Model):
    """Store validation results from Gemma model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    ]
    
    exercise = models.ForeignKey(JapaneseExercise, on_delete=models.CASCADE, related_name='validation_results')
    
    # Model being tested
    model_name = models.CharField(max_length=100, default='gemma:7b')
    provider = models.CharField(max_length=50, default='ollama')
    
    # Request/Response
    prompt_sent = models.TextField()
    gemma_response = models.TextField()
    
    # Validation results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_correct = models.BooleanField(null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True, help_text="0-1 score")
    validation_notes = models.TextField(blank=True)
    
    # Performance metrics
    response_time_ms = models.IntegerField(null=True, blank=True)
    token_count = models.IntegerField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.exercise.title} - {self.model_name} ({self.status})"


class TestSession(models.Model):
    """Group multiple validations into a session"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    model_name = models.CharField(max_length=100)
    provider = models.CharField(max_length=50)
    
    # Configuration
    config = models.JSONField(default=dict, help_text="Model configuration used")
    
    # Statistics
    total_tests = models.IntegerField(default=0)
    passed_tests = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def success_rate(self):
        if self.total_tests == 0:
            return 0
        return (self.passed_tests / self.total_tests) * 100
