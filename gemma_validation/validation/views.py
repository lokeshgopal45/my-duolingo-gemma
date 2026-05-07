"""
Views for validation API
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
import logging
import time

from .models import JapaneseExercise, GemmaValidationResult, TestSession
from .serializers import (
    JapaneseExerciseSerializer,
    GemmaValidationResultSerializer,
    TestSessionSerializer
)
from .llm_client import LLMClient, JapaneseExerciseValidator

logger = logging.getLogger(__name__)


class ExerciseViewSet(viewsets.ModelViewSet):
    """API endpoint for Japanese N3 exercises"""
    queryset = JapaneseExercise.objects.all()
    serializer_class = JapaneseExerciseSerializer
    search_fields = ['title', 'prompt', 'exercise_type']
    
    @action(detail=False, methods=['post'])
    def create_batch(self, request: Request):
        """Create multiple exercises at once"""
        exercises_data = request.data if isinstance(request.data, list) else request.data.get('exercises', [])
        serializer = JapaneseExerciseSerializer(data=exercises_data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'created': len(serializer.data), 'exercises': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request: Request):
        """Filter exercises by type"""
        exercise_type = request.query_params.get('type')
        if not exercise_type:
            return Response(
                {'error': 'type parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        exercises = self.queryset.filter(exercise_type=exercise_type)
        serializer = self.get_serializer(exercises, many=True)
        return Response(serializer.data)


class ValidationResultViewSet(viewsets.ModelViewSet):
    """API endpoint for validation results"""
    queryset = GemmaValidationResult.objects.all()
    serializer_class = GemmaValidationResultSerializer
    filterset_fields = ['exercise', 'model_name', 'status', 'is_correct']
    
    @action(detail=False, methods=['post'])
    def validate_exercise(self, request: Request):
        """Validate a single exercise using Gemma"""
        
        exercise_id = request.data.get('exercise_id')
        if not exercise_id:
            return Response(
                {'error': 'exercise_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            exercise = JapaneseExercise.objects.get(id=exercise_id)
        except JapaneseExercise.DoesNotExist:
            return Response(
                {'error': 'Exercise not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Initialize LLM client
        try:
            llm_client = LLMClient.from_settings()
            
            if not llm_client.is_available():
                return Response(
                    {'error': f'LLM service ({llm_client.provider}) not available at {llm_client.base_url}'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
        except Exception as e:
            logger.error(f"LLM initialization failed: {e}")
            return Response(
                {'error': f'LLM service error: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Create validator
        validator = JapaneseExerciseValidator(llm_client)
        
        # Build prompt
        prompt = validator.build_exercise_prompt(exercise)
        
        # Create result record
        result = GemmaValidationResult.objects.create(
            exercise=exercise,
            model_name=llm_client.model,
            provider=llm_client.provider,
            prompt_sent=prompt,
            status='processing'
        )
        
        try:
            # Query LLM
            start_time = time.time()
            gemma_response, metadata = llm_client.query(prompt)
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Validate response
            is_correct, confidence, notes = validator.validate_response(exercise, gemma_response)
            
            # Update result
            result.gemma_response = gemma_response
            result.status = 'completed'
            result.is_correct = is_correct
            result.confidence_score = confidence
            result.validation_notes = notes
            result.response_time_ms = response_time_ms
            result.save()
            
            serializer = GemmaValidationResultSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            result.status = 'error'
            result.validation_notes = str(e)
            result.save()
            
            return Response(
                {'error': f'Validation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def validate_batch(self, request: Request):
        """Validate multiple exercises in batch"""
        exercise_ids = request.data.get('exercise_ids', [])
        session_name = request.data.get('session_name', 'Batch Validation')
        
        if not exercise_ids:
            return Response(
                {'error': 'exercise_ids list required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize LLM client
        try:
            llm_client = LLMClient.from_settings()
            if not llm_client.is_available():
                return Response(
                    {'error': f'LLM service not available'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
        except Exception as e:
            return Response(
                {'error': f'LLM service error: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Create test session
        session = TestSession.objects.create(
            name=session_name,
            model_name=llm_client.model,
            provider=llm_client.provider,
            config={'temperature': 0.7}
        )
        
        validator = JapaneseExerciseValidator(llm_client)
        results = []
        passed = 0
        
        for exercise_id in exercise_ids:
            try:
                exercise = JapaneseExercise.objects.get(id=exercise_id)
                prompt = validator.build_exercise_prompt(exercise)
                
                result = GemmaValidationResult.objects.create(
                    exercise=exercise,
                    model_name=llm_client.model,
                    provider=llm_client.provider,
                    prompt_sent=prompt,
                    status='processing'
                )
                
                # Query LLM
                start_time = time.time()
                gemma_response, metadata = llm_client.query(prompt)
                response_time_ms = int((time.time() - start_time) * 1000)
                
                # Validate
                is_correct, confidence, notes = validator.validate_response(exercise, gemma_response)
                
                result.gemma_response = gemma_response
                result.status = 'completed'
                result.is_correct = is_correct
                result.confidence_score = confidence
                result.validation_notes = notes
                result.response_time_ms = response_time_ms
                result.save()
                
                if is_correct:
                    passed += 1
                
                results.append(GemmaValidationResultSerializer(result).data)
                
            except Exception as e:
                logger.error(f"Batch validation error for exercise {exercise_id}: {e}")
                continue
        
        # Update session stats
        session.total_tests = len(results)
        session.passed_tests = passed
        session.save()
        
        return Response({
            'session': TestSessionSerializer(session).data,
            'results': results,
            'summary': {
                'total': len(results),
                'passed': passed,
                'success_rate': (passed / len(results) * 100) if results else 0
            }
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request: Request):
        """Get validation statistics"""
        total_validations = GemmaValidationResult.objects.count()
        passed = GemmaValidationResult.objects.filter(is_correct=True).count()
        
        avg_confidence = 0
        results = GemmaValidationResult.objects.filter(confidence_score__isnull=False)
        if results.exists():
            avg_confidence = results.aggregate(avg=models.Avg('confidence_score'))['avg']
        
        by_type = {}
        for result in GemmaValidationResult.objects.select_related('exercise'):
            ex_type = result.exercise.exercise_type
            if ex_type not in by_type:
                by_type[ex_type] = {'total': 0, 'passed': 0}
            by_type[ex_type]['total'] += 1
            if result.is_correct:
                by_type[ex_type]['passed'] += 1
        
        return Response({
            'total_validations': total_validations,
            'passed': passed,
            'success_rate': (passed / total_validations * 100) if total_validations > 0 else 0,
            'avg_confidence': round(avg_confidence, 3),
            'by_exercise_type': by_type
        })
