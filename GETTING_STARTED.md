# 🚀 Getting Started with Gemma Validation

## Complete Setup Guide

This guide walks you through setting up the entire Gemma validation pipeline from scratch.

## Step 1: Install Prerequisites

### macOS
```bash
# Install Ollama (easiest option)
brew install ollama

# Or download from https://ollama.ai

# Install Python 3.9+
brew install python3

# Verify
python3 --version
ollama --version
```

### Linux
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Install Python
sudo apt-get install python3 python3-venv

# Verify
python3 --version
ollama serve  # Should start the server
```

### Windows
- Download Ollama: https://ollama.ai
- Download Python 3.9+: https://python.org
- Run installers and follow prompts
- Verify: Open PowerShell and type `ollama --version` and `python --version`

---

## Step 2: Download Gemma Model

### Option A: Using Ollama (Recommended)

```bash
# Terminal 1: Start Ollama service
ollama serve

# Terminal 2: Download Gemma
ollama pull gemma:7b

# You can also use gemma2
ollama pull gemma2:9b

# Verify
curl http://localhost:11434/api/tags
```

### Option B: Using LM Studio

1. Download LM Studio: https://lmstudio.ai/
2. Open LM Studio
3. Click the "Model Hub" icon on the left
4. Search for "gemma-4-e2b" or "gemma2"
5. Click download next to the model
6. Wait for download to complete
7. Go to "Local Server" tab
8. Select the model from dropdown
9. Click "Start Server" (runs on port 1234)

---

## Step 3: Set Up Python Environment

```bash
# Navigate to the project
cd /Users/lokeshgopal/XYZ/Projects/hackathons/my-duolingo-gemma

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Verify
which python  # Should show path to venv

# Install dependencies
pip install -r requirements.txt
```

---

## Step 4: Initialize Database & Load Data

```bash
# Navigate to validation directory
cd gemma_validation

# Create database
python manage.py migrate

# Load sample Japanese N3 exercises
python manage.py load_sample_exercises
```

---

## Step 5: Start the API Server

### Quick Start
```bash
python run_server.py
```

### Or Manual
```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

---

## Step 6: Test the Setup

### In Another Terminal

```bash
# Make sure you're in the gemma_validation directory and venv is activated

# Run tests
python test_validation.py
```

You should see:
```
============================================================
🔬 Gemma Validation Test Suite
============================================================

🔍 Testing LLM Connection...
   Provider: ollama
   URL: http://localhost:11434
   Model: gemma:7b
   ✅ LLM service is available!

📚 Loading Sample Exercises...
   ...
   
✅ All tests completed!
```

---

## Step 7: Try the API

### Check Available Exercises
```bash
curl http://localhost:8000/api/exercises/ | python -m json.tool
```

### Validate an Exercise
```bash
curl -X POST http://localhost:8000/api/results/validate_exercise/ \
  -H "Content-Type: application/json" \
  -d '{"exercise_id": 1}' | python -m json.tool
```

### Get Statistics
```bash
curl http://localhost:8000/api/results/statistics/ | python -m json.tool
```

---

## Step 8: Web Interface (Optional)

Django admin panel at: http://localhost:8000/admin/

Default credentials:
```bash
# Create superuser
python manage.py createsuperuser

# Then visit http://localhost:8000/admin/
```

---

## Common Workflows

### Validate All Exercises in a File

Create `validate_all.py`:
```python
import sys
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config')
django.setup()

from validation.models import JapaneseExercise
import requests

exercises = JapaneseExercise.objects.all()

for exercise in exercises:
    response = requests.post(
        'http://localhost:8000/api/results/validate_exercise/',
        json={'exercise_id': exercise.id}
    )
    result = response.json()
    status = "✅" if result['is_correct'] else "❌"
    print(f"{status} {exercise.title}: {result['confidence_score']:.0%}")
```

Run it:
```bash
python validate_all.py
```

### Add Custom Exercises

```python
from validation.models import JapaneseExercise

exercise = JapaneseExercise.objects.create(
    title="カスタム問題",
    exercise_type="grammar",
    jlpt_level="N3",
    prompt="質問です",
    context="",
    correct_answers=["答え1", "答え2"],
    explanation="解説です"
)
```

---

## Troubleshooting

### "Connection refused" for LLM

```bash
# Check if Ollama is running
ps aux | grep ollama

# If not, start it
ollama serve

# Test connection
curl http://localhost:11434/api/tags

# If using LM Studio on port 1234
curl http://localhost:1234/v1/models
```

### Django "Port already in use"

```bash
# Use different port
python manage.py runserver 8001

# Or kill the process
lsof -i :8000  # See what's using it
kill -9 <PID>   # Kill it
```

### Database locked

```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py load_sample_exercises
```

### LLM times out

Increase timeout in `.env`:
```env
LLM_TIMEOUT=300  # 5 minutes instead of 2
```

---

## Next Steps

1. **Add more exercises** - Expand with more N3 content
2. **Create frontend** - Build React UI for manual testing
3. **Add caching** - Cache responses for same prompts
4. **Integration** - Connect with Android/web app
5. **Performance** - Optimize prompt engineering
6. **Analytics** - Track validation trends

---

## Directory Layout

```
/Users/lokeshgopal/XYZ/Projects/hackathons/my-duolingo-gemma/
├── gemma_validation/          # Main Django project
│   ├── manage.py
│   ├── config.py              # Settings
│   ├── urls.py                # URL routing
│   ├── validation/            # Django app
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API views
│   │   ├── llm_client.py      # LLM integration
│   │   └── sample_data.py     # Sample exercises
│   ├── test_validation.py     # Test suite
│   ├── run_server.py          # Start server
│   ├── README.md              # API documentation
│   ├── API_EXAMPLES.md        # Usage examples
│   ├── .env                   # Environment config
│   └── db.sqlite3             # Database (auto-created)
├── OLLAMA_SETUP.md            # Ollama installation
├── requirements.txt           # Python dependencies
└── GETTING_STARTED.md         # This file
```

---

## Health Check Script

Create `health_check.py`:
```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000/api"
LLM_URL = os.getenv('LLM_BASE_URL', 'http://localhost:11434')

checks = []

# Check Django API
try:
    r = requests.get(f"{BASE_URL}/exercises/", timeout=5)
    checks.append(("Django API", r.status_code == 200))
except:
    checks.append(("Django API", False))

# Check LLM Service
try:
    r = requests.get(f"{LLM_URL}/api/tags", timeout=5)
    checks.append(("LLM Service", r.status_code == 200))
except:
    checks.append(("LLM Service", False))

# Print results
print("\n🏥 Health Check Results:\n")
for name, ok in checks:
    status = "✅" if ok else "❌"
    print(f"{status} {name}")

all_ok = all(ok for _, ok in checks)
print(f"\n{'✅ All systems operational' if all_ok else '❌ Some systems down'}\n")
```

Run: `python health_check.py`

---

## Quick Commands Reference

```bash
# Start everything
cd /Users/lokeshgopal/XYZ/Projects/hackathons/my-duolingo-gemma/gemma_validation
source ../venv/bin/activate
python run_server.py

# In another terminal
python test_validation.py

# Validate single exercise
curl -X POST http://localhost:8000/api/results/validate_exercise/ \
  -H "Content-Type: application/json" \
  -d '{"exercise_id": 1}'

# See all results
curl http://localhost:8000/api/results/

# Get stats
curl http://localhost:8000/api/results/statistics/
```

---

Good luck! 🎉
