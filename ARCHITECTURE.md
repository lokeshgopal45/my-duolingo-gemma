# System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    GEMMA VALIDATION SYSTEM                          │
└─────────────────────────────────────────────────────────────────────┘

                            ┌──────────────┐
                            │   Browser    │
                            │  (Optional)  │
                            └──────┬───────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
            ┌───────▼────────┐    HTTP       ┌───▼────────────┐
            │  cURL / Tests  │    REST       │  JavaScript    │
            │   (JSON)       │   Calls       │  (Fetch API)   │
            └───────┬────────┘              └───┬────────────┘
                    │                           │
                    └───────────┬────────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │   Django REST API       │
                    │  (Port 8000)            │
                    │                         │
                    │  ┌──────────────────┐  │
                    │  │ URL Routing      │  │
                    │  │  (/api/*)        │  │
                    │  └────────┬─────────┘  │
                    │           │            │
                    │  ┌────────▼──────────┐ │
                    │  │ REST ViewSets     │ │
                    │  │  - Exercises      │ │
                    │  │  - Validations    │ │
                    │  │  - Results        │ │
                    │  └────────┬──────────┘ │
                    │           │            │
                    │  ┌────────▼──────────┐ │
                    │  │ Serializers       │ │
                    │  │ JSON ↔ Python     │ │
                    │  └────────┬──────────┘ │
                    │           │            │
                    │  ┌────────▼──────────┐ │
                    │  │ Models (ORM)      │ │
                    │  │  - Exercise       │ │
                    │  │  - Result         │ │
                    │  │  - Session        │ │
                    │  └────────┬──────────┘ │
                    └───────────┼────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │  SQLite Database        │
                    │  (db.sqlite3)           │
                    │  - Exercises            │
                    │  - Validation Results   │
                    │  - Sessions & Stats     │
                    └─────────────────────────┘


         ┌─────────────────────────────────────────────┐
         │     LLM VALIDATION ENGINE                  │
         │                                             │
         │  ┌──────────────────────────────────────┐  │
         │  │  LLMClient (llm_client.py)           │  │
         │  │  - Ollama Adapter                    │  │
         │  │  - LM Studio Adapter                 │  │
         │  │  - Health Check                      │  │
         │  │  - Query Handler                     │  │
         │  └──────────┬───────────────────────────┘  │
         │             │                              │
         │  ┌──────────▼───────────────────────────┐  │
         │  │ JapaneseExerciseValidator            │  │
         │  │ - Build Prompts                      │  │
         │  │ - Exact Matching                     │  │
         │  │ - Semantic Verification              │  │
         │  │ - Confidence Scoring                 │  │
         │  └──────────┬───────────────────────────┘  │
         │             │                              │
         │  ┌──────────▼───────────────────────────┐  │
         │  │ Prompt Templates                     │  │
         │  │ - Reading Comprehension              │  │
         │  │ - Grammar Exercises                  │  │
         │  │ - Vocabulary Questions               │  │
         │  │ - Kanji Recognition                  │  │
         │  └──────────────────────────────────────┘  │
         └────────────┬────────────────────────────────┘
                      │
        ┌─────────────┴──────────────┐
        │                            │
   ┌────▼────────────┐       ┌──────▼────────────┐
   │  OLLAMA SERVER  │       │  LM STUDIO SERVER │
   │  (Port 11434)   │       │  (Port 1234)      │
   │                 │       │                   │
   │  Runs Gemma     │       │  Runs Gemma       │
   │  - 7B           │       │  - 4-E2B          │
   │  - 2B           │       │  - Other Models   │
   │                 │       │                   │
   │  REST API:      │       │  OpenAI compat:  │
   │  /api/generate  │       │  /v1/completions │
   │  /api/tags      │       │  /v1/models      │
   └────┬────────────┘       └──────┬────────────┘
        │                           │
   ┌────▼─────────────────────────▼─┐
   │      LOCAL GEMMA MODEL          │
   │   Running on Your Laptop        │
   │   (GPU/CPU Acceleration)        │
   │                                 │
   │  Japanese N3 Exercise Test      │
   │  Response Generation            │
   │                                 │
   └─────────────────────────────────┘


┌──────────────────────────────────────────────────────────┐
│            DATA FLOW - VALIDATION REQUEST                │
│                                                          │
│  1. User/Client                                          │
│     curl -X POST /api/results/validate_exercise/         │
│     {"exercise_id": 1}                                   │
│                                                          │
│  2. Django REST View                                     │
│     - Receives request                                   │
│     - Validates input                                    │
│     - Creates GemmaValidationResult record              │
│                                                          │
│  3. LLMClient                                            │
│     - Check LLM service availability                     │
│     - Prepare HTTP request (JSON)                        │
│                                                          │
│  4. Ollama/LM Studio                                     │
│     - Receives prompt                                    │
│     - Runs Gemma model                                   │
│     - Generates response (token by token)                │
│     - Returns complete response                          │
│                                                          │
│  5. JapaneseExerciseValidator                           │
│     - Exact matching check                               │
│     - LLM semantic verification                          │
│     - Calculate confidence score                         │
│                                                          │
│  6. Django Model                                         │
│     - Save result to database                            │
│     - Update statistics                                  │
│                                                          │
│  7. Response to Client                                   │
│     {                                                    │
│       "is_correct": true,                               │
│       "confidence_score": 0.92,                         │
│       "gemma_response": "...",                          │
│       "response_time_ms": 1245                          │
│     }                                                    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Key Components

### 1. **API Layer** (Django REST Framework)
- Routes HTTP requests to handlers
- Validates input/output
- Manages authentication/permissions
- Serializes data to/from JSON

### 2. **Business Logic** (Views & Validators)
- Exercise validation logic
- Prompt construction
- Response evaluation
- Confidence scoring

### 3. **LLM Integration** (LLMClient)
- Abstracts Ollama & LM Studio differences
- Health checks
- HTTP request/response handling
- Error management

### 4. **Data Layer** (Django ORM)
- Stores exercises, results, sessions
- Provides query interface
- Manages transactions

### 5. **LLM Engines**
- Ollama (local, lightweight)
- LM Studio (more features, UI)
- Both run Gemma models locally

---

## Data Models Relationships

```
JapaneseExercise
├─ id (PK)
├─ title
├─ exercise_type
├─ prompt
├─ correct_answers (JSON)
└─ (1 : N) ──→ GemmaValidationResult

GemmaValidationResult
├─ id (PK)
├─ exercise_id (FK) ──→ JapaneseExercise
├─ model_name
├─ gemma_response
├─ is_correct
├─ confidence_score
└─ response_time_ms

TestSession
├─ id (PK)
├─ name
├─ model_name
├─ total_tests
├─ passed_tests
└─ (tracks multiple validations)
```

---

## Request/Response Flow

```
REQUEST:
POST /api/results/validate_exercise/
{
  "exercise_id": 1
}

PROCESSING:
1. ViewSet receives request
2. Fetches JapaneseExercise(id=1)
3. Creates GemmaValidationResult (status=processing)
4. LLMClient queries Ollama
5. Validator processes response
6. Updates GemmaValidationResult with results

RESPONSE:
{
  "id": 42,
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
