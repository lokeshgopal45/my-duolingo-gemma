# Gemma Validation API - Django REST API

Complete Python/Django API for validating Gemma 4 E2B model responses on Japanese N3 exercises using Ollama or LM Studio.

## Quick Start

### 1. Prerequisites

- Python 3.8+
- Ollama or LM Studio installed and running
- Gemma model downloaded

### 2. Installation

```bash
# Navigate to the project
cd gemma_validation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or: venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r ../requirements.txt
```

### 3. Setup & Run

```bash
# Initialize database
python manage.py migrate

# Load sample Japanese N3 exercises
python manage.py load_sample_exercises

# Option A: Start development server
python manage.py runserver

# Option B: Use provided startup script
python run_server.py
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Exercises Management

**List Exercises**
```bash
GET /api/exercises/
```

**Get Exercise Details**
```bash
GET /api/exercises/{id}/
```

**Filter by Type**
```bash
GET /api/exercises/by_type/?type=grammar
```

**Create Exercise**
```bash
POST /api/exercises/
Content-Type: application/json

{
  "title": "文法テスト",
  "exercise_type": "grammar",
  "jlpt_level": "N3",
  "prompt": "___に最も適切な選択肢は？",
  "context": "",
  "correct_answers": ["A", "選択肢A"],
  "explanation": "解説です"
}
```

**Batch Create Exercises**
```bash
POST /api/exercises/create_batch/
Content-Type: application/json

{
  "exercises": [
    {exercise1},
    {exercise2}
  ]
}
```

### Validation & Testing

**Validate Single Exercise**
```bash
POST /api/results/validate_exercise/
Content-Type: application/json

{
  "exercise_id": 1
}
```

Response:
```json
{
  "id": 1,
  "exercise": 1,
  "exercise_title": "読解：短編小説",
  "model_name": "gemma:7b",
  "provider": "ollama",
  "prompt_sent": "与えられた文章を読んで...",
  "gemma_response": "会社を辞めてカフェを開いた",
  "status": "completed",
  "is_correct": true,
  "confidence_score": 0.92,
  "validation_notes": "Exact match found",
  "response_time_ms": 1245,
  "created_at": "2024-05-07T10:30:00Z"
}
```

**Batch Validation**
```bash
POST /api/results/validate_batch/
Content-Type: application/json

{
  "exercise_ids": [1, 2, 3],
  "session_name": "Daily N3 Validation"
}
```

**Get Validation Statistics**
```bash
GET /api/results/statistics/
```

Response:
```json
{
  "total_validations": 15,
  "passed": 12,
  "success_rate": 80.0,
  "avg_confidence": 0.856,
  "by_exercise_type": {
    "reading": {"total": 5, "passed": 4},
    "grammar": {"total": 5, "passed": 5},
    "vocabulary": {"total": 5, "passed": 3}
  }
}
```

## Testing

### Run Full Test Suite

```bash
python test_validation.py
```

This will:
1. Check LLM connection
2. Load sample exercises
3. Test single exercise validation
4. Run batch validation on 3 exercises
5. Display statistics

### Manual Testing with cURL

```bash
# Test LLM connection
curl http://localhost:8000/api/exercises/

# Validate an exercise
curl -X POST http://localhost:8000/api/results/validate_exercise/ \
  -H "Content-Type: application/json" \
  -d '{"exercise_id": 1}'

# Get statistics
curl http://localhost:8000/api/results/statistics/
```

## Configuration

Create a `.env` file in the root directory:

```env
# LLM Configuration
LLM_PROVIDER=ollama              # or lm_studio
LLM_BASE_URL=http://localhost:11434  # 11434 for Ollama, 1234 for LM Studio
LLM_MODEL=gemma:7b               # Model to use

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
LLM_TIMEOUT=120
```

## Project Structure

```
gemma_validation/
├── config.py              # Django settings
├── urls.py                # Main URL configuration
├── wsgi.py                # WSGI application
├── manage.py              # Django management script
├── run_server.py          # Server startup script
├── test_validation.py     # Test suite
├── validation/            # Django app
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── llm_client.py      # LLM integration
│   ├── sample_data.py     # Sample exercises
│   ├── admin.py           # Django admin
│   ├── apps.py            # App config
│   ├── urls.py            # App URLs
│   └── management/
│       └── commands/
│           └── load_sample_exercises.py
```

## Database

The API uses SQLite for simplicity. Database is stored at `db.sqlite3` in the project root.

### Reset Database

```bash
rm db.sqlite3
python manage.py migrate
python manage.py load_sample_exercises
```

## LLM Integration

### Ollama

```bash
# Pull model
ollama pull gemma:7b

# Start server
ollama serve

# Test
curl http://localhost:11434/api/tags
```

### LM Studio

1. Download from https://lmstudio.ai/
2. Download Gemma model in the UI
3. Click "Local Server" and configure:
   - Model: Select your Gemma
   - Port: 1234 (default)
4. Click "Start Server"

## Exercise Types

- **reading**: Reading comprehension
- **grammar**: Grammar exercises
- **vocabulary**: Vocabulary/word meaning
- **listening**: Listening comprehension
- **kanji**: Kanji reading and meaning

## Validation Logic

The validator:
1. **Exact Matching**: Checks for direct match with correct answers
2. **Semantic Verification**: Uses LLM to verify semantic correctness
3. **Confidence Scoring**: Returns 0-1 confidence score

## Metrics Tracked

- Response time (ms)
- Token count (if available)
- Confidence score (0-1)
- Success rate by exercise type
- Overall statistics

## Example Workflow

```python
from validation.llm_client import LLMClient, JapaneseExerciseValidator
from validation.models import JapaneseExercise

# Get an exercise
exercise = JapaneseExercise.objects.first()

# Initialize LLM client
llm = LLMClient.from_settings()

# Create validator
validator = JapaneseExerciseValidator(llm)

# Build prompt
prompt = validator.build_exercise_prompt(exercise)

# Get response
response, metadata = llm.query(prompt)

# Validate
is_correct, confidence, notes = validator.validate_response(
    exercise, 
    response
)

print(f"Correct: {is_correct}, Confidence: {confidence}")
```

## Production Deployment

For production:
1. Set `DEBUG=False` in `.env`
2. Use a production database (PostgreSQL recommended)
3. Use gunicorn: `gunicorn config.wsgi`
4. Set up nginx reverse proxy
5. Configure proper secret key and allowed hosts

## Troubleshooting

### "LLM service not available"
- Check if Ollama/LM Studio is running
- Verify the base URL in `.env`
- Test with: `curl <LLM_BASE_URL>/api/tags` (Ollama) or `/v1/models` (LM Studio)

### Slow responses
- Reduce batch size
- Increase `LLM_TIMEOUT` if needed
- Check LLM GPU utilization
- Use a smaller model

### Database errors
- Ensure SQLite is available
- Check file permissions
- Run `python manage.py migrate` again

## Contributing

Add new exercise types:
1. Create new exercise in `sample_data.py`
2. Update validation logic in `llm_client.py` if needed
3. Add tests in `test_validation.py`

## License

Part of the my-duolingo-gemma project
