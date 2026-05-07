# 🎯 Gemma Validation Project - Complete Overview

**Status**: ✅ Ready to Use  
**Last Updated**: May 2024  
**Purpose**: Validate Google Gemma 4 E2B model on Japanese N3 language exercises

---

## 📚 Documentation Guide

Start here based on your role:

### 👤 For Users / First-Time Setup
1. **[GETTING_STARTED.md](GETTING_STARTED.md)** ← **START HERE**
   - Step-by-step installation
   - Environment setup
   - First test
   - Troubleshooting

### 👨‍💻 For Developers
1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview & structure
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design & data flow
3. **[gemma_validation/README.md](gemma_validation/README.md)** - API documentation
4. **[gemma_validation/API_EXAMPLES.md](gemma_validation/API_EXAMPLES.md)** - Code examples

### 🔧 For Setup/DevOps
1. **[OLLAMA_SETUP.md](OLLAMA_SETUP.md)** - LLM server installation
2. **[setup.sh](setup.sh)** or **[setup.bat](setup.bat)** - Automated setup
3. **[requirements.txt](requirements.txt)** - Python dependencies

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Run setup
bash setup.sh              # macOS/Linux
# OR: setup.bat           # Windows

# 2. Start LLM server (new terminal)
ollama serve

# 3. Start API server (another terminal)
cd gemma_validation
python run_server.py

# 4. Test (another terminal)
python test_validation.py

# 5. Access API
curl http://localhost:8000/api/exercises/
```

---

## 📂 Directory Structure

```
my-duolingo-gemma/
│
├── 📄 GETTING_STARTED.md       ← Start here!
├── 📄 PROJECT_SUMMARY.md       ← Project overview
├── 📄 ARCHITECTURE.md          ← System design
├── 📄 OLLAMA_SETUP.md          ← LLM setup
├── 📄 DOCUMENTATION_INDEX.md   ← This file
│
├── 📋 requirements.txt          ← Python dependencies
├── 🔧 setup.sh & setup.bat     ← Automated setup
│
└── 📁 gemma_validation/         ← Main Django project
    │
    ├── 📄 README.md            ← API docs
    ├── 📄 API_EXAMPLES.md      ← Code examples
    ├── 📄 .env                 ← Configuration
    ├── 📄 .env.example         ← Example config
    │
    ├── 🐍 manage.py            ← Django CLI
    ├── 🐍 run_server.py        ← Start server
    ├── 🐍 test_validation.py   ← Test suite
    │
    ├── 📁 validation/          ← Django app
    │   ├── models.py           ← Database models
    │   ├── views.py            ← API endpoints
    │   ├── serializers.py      ← JSON serialization
    │   ├── llm_client.py       ← LLM integration
    │   ├── sample_data.py      ← Sample exercises
    │   ├── admin.py            ← Django admin
    │   ├── urls.py             ← URL routing
    │   └── management/         ← Management commands
    │       └── commands/
    │           └── load_sample_exercises.py
    │
    ├── 📁 config.py            ← Django settings
    ├── 📁 urls.py              ← Main URL config
    ├── 📁 wsgi.py & asgi.py   ← App servers
    │
    └── 📁 db.sqlite3           ← Database (auto-created)
```

---

## 🎯 What You Can Do

### 1. **Validate Single Exercise**
```bash
curl -X POST http://localhost:8000/api/results/validate_exercise/ \
  -H "Content-Type: application/json" \
  -d '{"exercise_id": 1}'
```

### 2. **Batch Validate Multiple Exercises**
```bash
curl -X POST http://localhost:8000/api/results/validate_batch/ \
  -H "Content-Type: application/json" \
  -d '{
    "exercise_ids": [1, 2, 3, 4, 5],
    "session_name": "Daily Test"
  }'
```

### 3. **Get Validation Statistics**
```bash
curl http://localhost:8000/api/results/statistics/ | jq
```

### 4. **Create Custom Exercises**
```bash
curl -X POST http://localhost:8000/api/exercises/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "新しい問題",
    "exercise_type": "grammar",
    "jlpt_level": "N3",
    "prompt": "質問です",
    "correct_answers": ["答え1"],
    "explanation": "解説です"
  }'
```

### 5. **Get All Exercises**
```bash
curl http://localhost:8000/api/exercises/ | jq
```

---

## 📊 Features

✅ **LLM Integration**
- Ollama support (lightweight, easy)
- LM Studio support (feature-rich)
- Automatic service detection
- Health checks

✅ **Exercise Management**
- 8 sample Japanese N3 exercises included
- Create/read/update/delete exercises
- Filter by type (reading, grammar, vocabulary, kanji, listening)
- Batch operations

✅ **Validation Engine**
- Exact answer matching
- Semantic verification using LLM
- Confidence scoring (0-1)
- Performance metrics tracking

✅ **REST API**
- Full CRUD operations
- Batch processing
- Statistics & analytics
- JSON responses

✅ **Database**
- SQLite (built-in, no setup)
- Django ORM (no SQL needed)
- Easy to migrate to PostgreSQL

✅ **Testing & Debugging**
- Comprehensive test suite
- Admin panel for data inspection
- Example API calls
- Detailed logging

---

## 🚀 Typical Workflow

### Day 1: Setup
1. Run `setup.sh` or `setup.bat`
2. Start Ollama with `ollama serve`
3. Start API with `python run_server.py`
4. Run tests with `python test_validation.py`

### Day 2+: Use the API
1. Add your Japanese exercises
2. Call validate endpoints
3. Monitor statistics
4. Adjust prompts/logic based on results

### Production:
1. Set DEBUG=False in .env
2. Use PostgreSQL instead of SQLite
3. Deploy with gunicorn/nginx
4. Set up monitoring/logging

---

## 🔑 Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/exercises/` | GET | List exercises |
| `/api/exercises/` | POST | Create exercise |
| `/api/exercises/{id}/` | GET | Get exercise |
| `/api/exercises/by_type/?type=grammar` | GET | Filter by type |
| `/api/results/validate_exercise/` | POST | Validate one |
| `/api/results/validate_batch/` | POST | Validate many |
| `/api/results/statistics/` | GET | Get stats |

---

## ⚙️ Configuration

### Environment Variables (`.env` file)

```env
# LLM Settings
LLM_PROVIDER=ollama              # ollama or lm_studio
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=gemma:7b
LLM_TIMEOUT=120

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Changing LLM Provider

**To use LM Studio instead of Ollama:**
```env
LLM_PROVIDER=lm_studio
LLM_BASE_URL=http://localhost:1234
LLM_MODEL=gemma-4-e2b-it
```

---

## 🧪 Testing

### Run Full Test Suite
```bash
cd gemma_validation
python test_validation.py
```

### Manual Testing
```bash
# Check LLM connection
curl http://localhost:11434/api/tags

# Check API
curl http://localhost:8000/api/exercises/

# Validate exercise
curl -X POST http://localhost:8000/api/results/validate_exercise/ \
  -H "Content-Type: application/json" \
  -d '{"exercise_id": 1}'
```

### Python Testing
```python
import requests

# Get an exercise
ex = requests.get('http://localhost:8000/api/exercises/').json()[0]

# Validate it
result = requests.post(
    'http://localhost:8000/api/results/validate_exercise/',
    json={'exercise_id': ex['id']}
).json()

print(f"Correct: {result['is_correct']}")
print(f"Confidence: {result['confidence_score']:.0%}")
```

---

## 📝 Database Schema

### JapaneseExercise
```python
{
  id: int,                          # Primary key
  title: str,                       # Exercise title
  exercise_type: str,               # reading|grammar|vocabulary|kanji|listening
  jlpt_level: str,                 # N3, N2, N1, etc.
  prompt: str,                      # The question
  context: str,                     # Background info (for reading)
  correct_answers: list,            # List of acceptable answers
  explanation: str,                 # Answer explanation
  created_at: datetime,
  updated_at: datetime
}
```

### GemmaValidationResult
```python
{
  id: int,
  exercise_id: int,                 # FK to JapaneseExercise
  model_name: str,                  # gemma:7b, etc.
  provider: str,                    # ollama or lm_studio
  prompt_sent: str,                 # Exact prompt sent to LLM
  gemma_response: str,              # Model's response
  status: str,                      # pending|processing|completed|error
  is_correct: bool,                 # Validation result
  confidence_score: float,          # 0.0-1.0
  validation_notes: str,            # Why correct/incorrect
  response_time_ms: int,            # How long LLM took
  token_count: int,                 # Number of tokens
  created_at: datetime,
  updated_at: datetime
}
```

### TestSession
```python
{
  id: int,
  name: str,                        # Session name
  description: str,
  model_name: str,
  provider: str,
  config: dict,                     # Model config (JSON)
  total_tests: int,
  passed_tests: int,
  created_at: datetime,
  updated_at: datetime
  
  # Computed property
  success_rate: float               # (passed / total) * 100
}
```

---

## 🔍 Troubleshooting

### Problem: "LLM service not available"
**Solution:**
```bash
# Start Ollama
ollama serve

# Or start LM Studio from GUI
```

### Problem: "Port 8000 already in use"
**Solution:**
```bash
# Use different port
python manage.py runserver 8001
```

### Problem: "ModuleNotFoundError"
**Solution:**
```bash
# Activate venv and reinstall
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: Database errors
**Solution:**
```bash
cd gemma_validation
rm db.sqlite3
python manage.py migrate
python manage.py load_sample_exercises
```

See [GETTING_STARTED.md](GETTING_STARTED.md) for more troubleshooting.

---

## 📚 Learning Resources

### Understanding the Code
1. **models.py** - Start here to understand data structures
2. **llm_client.py** - See how it talks to Ollama/LM Studio
3. **views.py** - REST API endpoint logic
4. **sample_data.py** - See example exercises

### Running Examples
- **test_validation.py** - Full working example
- **API_EXAMPLES.md** - Copy-paste ready code
- **GETTING_STARTED.md** - Step-by-step walkthroughs

---

## 🎓 Common Use Cases

### 1. Test a New Model
```bash
# In .env, change:
LLM_MODEL=gemma2:9b
# Then: python test_validation.py
```

### 2. Validate Production Dataset
```bash
curl -X POST http://localhost:8000/api/results/validate_batch/ \
  -H "Content-Type: application/json" \
  -d '{
    "exercise_ids": [1,2,3,4,5,6,7,8],
    "session_name": "Production Validation"
  }' > results.json
```

### 3. Track Performance Over Time
```bash
# Run tests daily
0 0 * * * cd ~/project && python gemma_validation/test_validation.py >> logs.txt
```

### 4. Find Problem Exercises
```bash
# SQL: Find lowest confidence scores
SELECT exercise_id, COUNT(*) as attempts, 
       AVG(confidence_score) as avg_confidence
FROM validation_gemmavalidationresult
GROUP BY exercise_id
ORDER BY avg_confidence ASC
LIMIT 10;
```

---

## 🚀 Next Steps

### Short Term (This Week)
- [ ] Complete setup (GETTING_STARTED.md)
- [ ] Run test suite successfully
- [ ] Validate 5-10 exercises manually
- [ ] Review validation results

### Medium Term (This Month)
- [ ] Add 20+ more Japanese exercises
- [ ] Benchmark with different Gemma models
- [ ] Optimize prompts based on results
- [ ] Set up automated daily tests

### Long Term (Next Month+)
- [ ] Build web UI for manual testing
- [ ] Integrate with Android app
- [ ] Deploy to cloud server
- [ ] Add more language levels (N4, N2, N1)
- [ ] Track student progress if applicable

---

## 📞 Support & Help

### Getting Stuck?
1. Check [GETTING_STARTED.md](GETTING_STARTED.md#troubleshooting) - Most issues covered
2. Run `python test_validation.py` - Diagnostic test
3. Check [API_EXAMPLES.md](gemma_validation/API_EXAMPLES.md) - Working code
4. Review [ARCHITECTURE.md](ARCHITECTURE.md) - How it works

### Common Issues
- **LLM not responding** → Check `ollama serve` is running
- **API won't start** → Check port 8000 is free
- **Database errors** → Delete `db.sqlite3` and reinit
- **Import errors** → Activate venv and reinstall

---

## ✅ Verification Checklist

Before considering setup complete:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] .env file created with settings
- [ ] Ollama/LM Studio installed and running
- [ ] Gemma model downloaded
- [ ] Database initialized (`python manage.py migrate`)
- [ ] Sample data loaded (`python manage.py load_sample_exercises`)
- [ ] API server starts (`python run_server.py`)
- [ ] Test suite passes (`python test_validation.py`)
- [ ] Can access http://localhost:8000/api/exercises/

---

## 📞 Quick Reference

### Start Servers
```bash
# Terminal 1: LLM
ollama serve

# Terminal 2: API
cd gemma_validation
python run_server.py

# Terminal 3: Tests
cd gemma_validation
python test_validation.py
```

### Common Commands
```bash
# Setup
bash setup.sh

# Run tests
python test_validation.py

# Load exercises
python manage.py load_sample_exercises

# Reset database
rm db.sqlite3 && python manage.py migrate

# Django shell (explore data)
python manage.py shell

# API documentation
http://localhost:8000/api/

# Admin panel
http://localhost:8000/admin/
```

---

## 📄 License

Part of the my-duolingo-gemma project

---

## 🎉 Ready to Start?

→ **Open [GETTING_STARTED.md](GETTING_STARTED.md) now!**

Or if you're familiar with Django and APIs, check:
→ **[gemma_validation/README.md](gemma_validation/README.md)**

Good luck! 🚀
