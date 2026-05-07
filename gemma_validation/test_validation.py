"""
Test script to validate Gemma responses on Japanese N3 exercises
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from validation.models import JapaneseExercise, GemmaValidationResult
from validation.llm_client import LLMClient, JapaneseExerciseValidator
from validation.sample_data import load_sample_exercises
import json


def test_llm_connection():
    """Test if LLM service is available"""
    print("\n🔍 Testing LLM Connection...")
    
    llm = LLMClient.from_settings()
    print(f"   Provider: {llm.provider}")
    print(f"   URL: {llm.base_url}")
    print(f"   Model: {llm.model}")
    
    if llm.is_available():
        print("   ✅ LLM service is available!")
        return True
    else:
        print("   ❌ LLM service is NOT available!")
        print(f"   Make sure {llm.provider} is running at {llm.base_url}")
        return False


def load_exercises():
    """Load sample exercises"""
    print("\n📚 Loading Sample Exercises...")
    
    count = load_sample_exercises()
    total = JapaneseExercise.objects.count()
    
    print(f"   Created: {count} new exercises")
    print(f"   Total: {total} exercises in database")
    
    # Show available exercises
    by_type = JapaneseExercise.objects.values('exercise_type').distinct()
    for item in by_type:
        type_name = item['exercise_type']
        count = JapaneseExercise.objects.filter(exercise_type=type_name).count()
        print(f"   - {type_name}: {count}")


def test_single_exercise(exercise_id=None):
    """Test a single exercise"""
    print("\n🧪 Testing Single Exercise...")
    
    if not exercise_id:
        exercise = JapaneseExercise.objects.first()
    else:
        exercise = JapaneseExercise.objects.get(id=exercise_id)
    
    if not exercise:
        print("   ❌ No exercises found")
        return
    
    print(f"   Exercise: {exercise.title}")
    print(f"   Type: {exercise.exercise_type}")
    print(f"   Prompt: {exercise.prompt[:100]}...")
    
    llm = LLMClient.from_settings()
    validator = JapaneseExerciseValidator(llm)
    
    # Build prompt
    prompt = validator.build_exercise_prompt(exercise)
    print(f"\n   Sending to LLM...")
    
    try:
        response, metadata = llm.query(prompt)
        print(f"   ✅ Response received ({metadata['elapsed_ms']}ms)")
        print(f"   Response: {response[:200]}...")
        
        # Validate
        is_correct, confidence, notes = validator.validate_response(exercise, response)
        print(f"\n   Validation Result:")
        print(f"   - Correct: {is_correct}")
        print(f"   - Confidence: {confidence:.2%}")
        print(f"   - Notes: {notes}")
        
        # Save result
        result = GemmaValidationResult.objects.create(
            exercise=exercise,
            model_name=llm.model,
            provider=llm.provider,
            prompt_sent=prompt,
            gemma_response=response,
            status='completed',
            is_correct=is_correct,
            confidence_score=confidence,
            validation_notes=notes,
            response_time_ms=metadata['elapsed_ms']
        )
        print(f"   ✅ Result saved (ID: {result.id})")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")


def test_batch_validation(count=3):
    """Test batch validation"""
    print(f"\n🚀 Testing Batch Validation ({count} exercises)...")
    
    exercises = JapaneseExercise.objects.all()[:count]
    
    if not exercises:
        print("   ❌ No exercises found")
        return
    
    llm = LLMClient.from_settings()
    validator = JapaneseExerciseValidator(llm)
    
    results = []
    passed = 0
    
    for i, exercise in enumerate(exercises, 1):
        print(f"\n   [{i}/{count}] {exercise.title}")
        
        try:
            prompt = validator.build_exercise_prompt(exercise)
            response, metadata = llm.query(prompt)
            is_correct, confidence, notes = validator.validate_response(exercise, response)
            
            result = GemmaValidationResult.objects.create(
                exercise=exercise,
                model_name=llm.model,
                provider=llm.provider,
                prompt_sent=prompt,
                gemma_response=response,
                status='completed',
                is_correct=is_correct,
                confidence_score=confidence,
                validation_notes=notes,
                response_time_ms=metadata['elapsed_ms']
            )
            
            status_emoji = "✅" if is_correct else "❌"
            print(f"       {status_emoji} Correct: {is_correct}, Confidence: {confidence:.0%}")
            
            results.append(result)
            if is_correct:
                passed += 1
                
        except Exception as e:
            print(f"       ❌ Error: {e}")
    
    # Summary
    print(f"\n   Summary:")
    print(f"   - Total: {len(results)}")
    print(f"   - Passed: {passed}")
    print(f"   - Failed: {len(results) - passed}")
    print(f"   - Success Rate: {(passed / len(results) * 100):.1f}%")


def show_statistics():
    """Show validation statistics"""
    print("\n📊 Validation Statistics...")
    
    total = GemmaValidationResult.objects.count()
    if total == 0:
        print("   No validation results yet")
        return
    
    passed = GemmaValidationResult.objects.filter(is_correct=True).count()
    failed = total - passed
    
    print(f"   Total Validations: {total}")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print(f"   Success Rate: {(passed / total * 100):.1f}%")
    
    # By type
    print(f"\n   By Exercise Type:")
    by_type = {}
    for result in GemmaValidationResult.objects.select_related('exercise'):
        ex_type = result.exercise.exercise_type
        if ex_type not in by_type:
            by_type[ex_type] = {'total': 0, 'passed': 0}
        by_type[ex_type]['total'] += 1
        if result.is_correct:
            by_type[ex_type]['passed'] += 1
    
    for ex_type, stats in by_type.items():
        rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"   - {ex_type}: {stats['passed']}/{stats['total']} ({rate:.1f}%)")


def main():
    """Main test runner"""
    print("=" * 60)
    print("🔬 Gemma Validation Test Suite")
    print("=" * 60)
    
    # Test LLM connection
    if not test_llm_connection():
        print("\n⚠️  Skipping validation tests (LLM not available)")
        print("   Make sure Ollama or LM Studio is running!")
        sys.exit(1)
    
    # Load exercises
    load_exercises()
    
    # Run tests
    try:
        print("\nRunning tests...")
        test_single_exercise()
        test_batch_validation(count=3)
        show_statistics()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
