"""
Views for validation API
"""
import json
import logging
import re
import time

from django.db import models
from requests.exceptions import RequestException
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .llm_client import LLMClient, JapaneseExerciseValidator
from .models import GemmaValidationResult, JapaneseExercise, TestSession
from .serializers import (
    ChoiceValidationRequestSerializer,
    GemmaValidationResultSerializer,
    JapaneseExerciseSerializer,
    TestSessionSerializer,
)

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

    def _normalize_text(self, value: str) -> str:
        return re.sub(r"\s+", " ", str(value)).strip().lower()

    def _match_option(self, candidate: str, options: list[str]) -> str | None:
        normalized_candidate = self._normalize_text(candidate)
        for option in options:
            if normalized_candidate == self._normalize_text(option):
                return option
        for option in options:
            if normalized_candidate in self._normalize_text(option):
                return option
        return None

    def _extract_choice(self, response: str, options: list[str]) -> str | None:
        normalized_response = self._normalize_text(response)

        try:
            parsed = json.loads(response)
            if isinstance(parsed, dict):
                for key in ('answer', 'choice', 'selected_answer', 'correct_answer'):
                    candidate = parsed.get(key)
                    if isinstance(candidate, str):
                        resolved = self._match_option(candidate, options)
                        if resolved:
                            return resolved
        except json.JSONDecodeError:
            pass

        for option in options:
            if self._normalize_text(option) in normalized_response:
                return option

        label_match = re.search(r"\b([A-D])\b", response, flags=re.IGNORECASE)
        if label_match:
            index = ord(label_match.group(1).upper()) - ord('A')
            if 0 <= index < len(options):
                return options[index]

        numbered_match = re.search(r"\b([1-9])\b", response)
        if numbered_match:
            index = int(numbered_match.group(1)) - 1
            if 0 <= index < len(options):
                return options[index]

        return None

    @action(detail=False, methods=['post'])
    def validate_choice(self, request: Request):
        """Validate a multiple-choice answer against Gemma."""

        serializer = ChoiceValidationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        try:
            llm_client = LLMClient.from_settings()

            if not llm_client.is_available():
                return Response(
                    {'error': f'LLM service ({llm_client.provider}) not available at {llm_client.base_url}'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
        except (AttributeError, OSError, ValueError) as e:
            logger.error('LLM initialization failed: %s', e)
            return Response(
                {'error': f'LLM service error: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        prompt_lines = [
            f"Section: {payload['section']}",
            f"Question: {payload['question']}",
            "Options:",
        ]

        for index, option in enumerate(payload['options'], start=1):
            prompt_lines.append(f"{index}. {option}")

        prompt_lines.extend([
            f"Student selected: {payload['selected_answer']}",
            f"Reference correct answer: {payload['correct_answer']}",
            payload.get('explanation') or '',
            '',
            'Return only the single best option text that answers the question.',
            'Do not explain your reasoning.',
        ])

        prompt = "\n".join(line for line in prompt_lines if line is not None)

        try:
            start_time = time.time()
            gemma_response, _metadata = llm_client.query(prompt, temperature=0.2)
            response_time_ms = int((time.time() - start_time) * 1000)

            gemma_choice = self._extract_choice(gemma_response, payload['options'])
            selected_answer = payload['selected_answer']
            correct_answer = payload['correct_answer']

            is_correct = self._match_option(selected_answer, [correct_answer]) is not None
            gemma_agrees = self._match_option(gemma_choice or '', [correct_answer]) is not None
            confidence = 0.9 if gemma_agrees else 0.55 if gemma_choice else 0.4

            notes = (
                f"Gemma chose {gemma_choice or 'an unclear answer'}; "
                f"reference answer is {correct_answer}."
            )

            return Response({
                'section': payload['section'],
                'question': payload['question'],
                'selected_answer': selected_answer,
                'correct_answer': correct_answer,
                'gemma_answer': gemma_choice,
                'gemma_response': gemma_response,
                'is_correct': is_correct,
                'gemma_agrees': gemma_agrees,
                'confidence_score': confidence,
                'validation_notes': notes,
                'response_time_ms': response_time_ms,
                'model_name': llm_client.model,
                'provider': llm_client.provider,
            }, status=status.HTTP_200_OK)

        except (RequestException, OSError, ValueError) as e:
            logger.error('Choice validation failed: %s', e)
            return Response(
                {'error': f'Validation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
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
        except (AttributeError, OSError, ValueError) as e:
            logger.error('LLM initialization failed: %s', e)
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
            gemma_response, _metadata = llm_client.query(prompt)
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
            
        except (RequestException, OSError, ValueError) as e:
            logger.error('Validation failed: %s', e)
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
                    {'error': 'LLM service not available'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
        except (AttributeError, OSError, ValueError) as e:
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
                gemma_response, _metadata = llm_client.query(prompt)
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
                
            except (RequestException, OSError, ValueError) as e:
                logger.error('Batch validation error for exercise %s: %s', exercise_id, e)
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
    def statistics(self, _request: Request):
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
