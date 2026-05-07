# 🚀 Gemma Validation - Quick Reference Card

## One-Liner Setup
```bash
bash setup.sh && cd gemma_validation && python run_server.py
# (in another terminal: ollama serve)
```

---

## 📍 File Locations

| What | Location |
|------|----------|
| Main API | `http://localhost:8000/api/` |
| Admin Panel | `http://localhost:8000/admin/` |
| Setup Script | `setup.sh` or `setup.bat` |
| Django Project | `gemma_validation/` |
| Database | `gemma_validation/db.sqlite3` |
| Configuration | `gemma_validation/.env` |
| Tests | `gemma_validation/test_validation.py` |
| Documentation | `GETTING_STARTED.md` |

---

## 🔌 Essential API Calls

### List Exercises
```bash
curl http://localhost:8000/api/exercises/
```

### Validate Exercise
```bash
curl -X POST http://localhost:8000/api/results/validate_exercise/ \
  -H "Content-Type: application/json" \
  -d '{"exercise_id": 1}'
```

### Batch Validate
```bash
curl -X POST http://localhost:8000/api/results/validate_batch/ \
  -H "Content-Type: application/json" \
  -d '{"exercise_ids": [1,2,3], "session_name": "Test"}'
```

### Get Statistics
```bash
curl http://localhost:8000/api/results/statistics/
```

---

## 🐍 Python Quick Examples

### Validate and Check Result
```python
import requests

result = requests.post(
    'http://localhost:8000/api/results/validate_exercise/',
    json={'exercise_id': 1}
).json()

print(f"Correct: {result['is_correct']}")
print(f"Confidence: {result['confidence_score']:.0%}")
print(f"Response: {result['gemma_response']}")
```

### Get All Exercises
```python
import requests

exercises = requests.get('http://localhost:8000/api/exercises/').json()
for ex in exercises:
    print(f"{ex['id']}: {ex['title']} ({ex['exercise_type']})")
```

### Get Statistics
```python
import requests

stats = requests.get('http://localhost:8000/api/results/statistics/').json()
print(f"Success Rate: {stats['success_rate']:.1f}%")
print(f"Total Tests: {stats['total_validations']}")
```

---

## ⚙️ Configuration

### Switch LLM Provider
**For LM Studio (instead of Ollama):**
Edit `gemma_validation/.env`:
```env
LLM_PROVIDER=lm_studio
LLM_BASE_URL=http://localhost:1234
LLM_MODEL=gemma-4-e2b-it
```

### Increase Timeout
If LLM is slow:
```env
LLM_TIMEOUT=300
```

---

## 🧪 Testing

### Run Full Tests
```bash
cd gemma_validation
python test_validation.py
```

### Check LLM Connection
```bash
# For Ollama
curl http://localhost:11434/api/tags

# For LM Studio
curl http://localhost:1234/v1/models
```

### Check API
```bash
curl http://localhost:8000/api/exercises/
```

---

## 🔧 Troubleshooting

### LLM Not Working
```bash
# Start Ollama (Terminal 1)
ollama serve

# If using LM Studio: Open GUI and click "Start Server"
```

### Port 8000 In Use
```bash
# Use different port
python manage.py runserver 8001
```

### Database Issues
```bash
cd gemma_validation
rm db.sqlite3
python manage.py migrate
python manage.py load_sample_exercises
```

### Python Errors
```bash
# Activate venv
source venv/bin/activate  # or: venv\Scripts\activate

# Reinstall
pip install -r requirements.txt
```

---

## 📂 Key Files

| File | Purpose |
|------|---------|
| `config.py` | Django settings |
| `validation/models.py` | Database schemas |
| `validation/views.py` | API endpoints |
| `validation/llm_client.py` | LLM integration |
| `validation/sample_data.py` | Sample exercises |
| `test_validation.py` | Test suite |
| `.env` | Configuration |

---

## 📊 Database Operations

### Create Exercise (via Django shell)
```bash
python manage.py shell
```

```python
from validation.models import JapaneseExercise

JapaneseExercise.objects.create(
    title="新しい問題",
    exercise_type="grammar",
    jlpt_level="N3",
    prompt="質問",
    correct_answers=["答え1"],
    explanation="解説"
)
```

### View Results
```python
from validation.models import GemmaValidationResult

results = GemmaValidationResult.objects.all()
for r in results:
    print(f"{r.exercise.title}: {r.is_correct}")
```

### Clear Results
```python
GemmaValidationResult.objects.all().delete()
```

---

## 🎯 Typical Session

```bash
# Terminal 1: Start LLM
ollama serve

# Terminal 2: Start API
cd gemma_validation
python run_server.py

# Terminal 3: Run tests/curl
python test_validation.py

# OR: Make API calls
curl http://localhost:8000/api/exercises/ | jq
```

---

## 📈 Performance Tips

### Speed Up Responses
```env
LLM_MODEL=gemma:7b          # Smaller model
# Reduce timeout if needed
```

### Batch Process
Instead of validating one-by-one, use batch:
```bash
curl -X POST http://localhost:8000/api/results/validate_batch/ \
  -H "Content-Type: application/json" \
  -d '{"exercise_ids": [1,2,3,4,5]}'
```

### Enable GPU (Ollama)
```bash
# Ollama auto-enables GPU if available
# Check with: ollama show gemma:7b | grep parameters
```

---

## 🚀 Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Run `gunicorn config.wsgi`
- [ ] Set up nginx reverse proxy
- [ ] Configure SSL/HTTPS
- [ ] Set strong SECRET_KEY
- [ ] Update ALLOWED_HOSTS
- [ ] Enable logging
- [ ] Set up monitoring

---

## 📚 Documentation Files

| File | Read If... |
|------|-----------|
| GETTING_STARTED.md | First time setup |
| gemma_validation/README.md | Want API docs |
| gemma_validation/API_EXAMPLES.md | Need code examples |
| ARCHITECTURE.md | Want to understand design |
| OLLAMA_SETUP.md | Setting up LLM |
| PROJECT_SUMMARY.md | Need overview |

---

## 🆘 Quick Help

```bash
# See all exercises
curl http://localhost:8000/api/exercises/

# Validate one
curl -X POST http://localhost:8000/api/results/validate_exercise/ \
  -H "Content-Type: application/json" \
  -d '{"exercise_id": 1}'

# See results
curl http://localhost:8000/api/results/

# See stats
curl http://localhost:8000/api/results/statistics/

# Run tests
python test_validation.py

# Reset everything
rm db.sqlite3 && python manage.py migrate && python manage.py load_sample_exercises
```

---

## 💡 Pro Tips

1. **Pretty JSON Output**
   ```bash
   curl ... | jq
   ```

2. **Save Results to File**
   ```bash
   curl ... > results.json
   ```

3. **Test in Python REPL**
   ```bash
   python manage.py shell
   ```

4. **View Database in Admin**
   ```bash
   http://localhost:8000/admin/
   # Create superuser first: python manage.py createsuperuser
   ```

5. **Batch Validation in Python**
   ```python
   exercises = [1,2,3,4,5]
   for ex_id in exercises:
       result = requests.post(
           'http://localhost:8000/api/results/validate_exercise/',
           json={'exercise_id': ex_id}
       ).json()
       print(f"#{ex_id}: {result['is_correct']}")
   ```

---

## ⏱️ Expected Times

| Operation | Time |
|-----------|------|
| Setup.sh | ~2 min |
| First validation | ~5-10 sec |
| Batch (5 exercises) | ~30-50 sec |
| Full test suite | ~2-3 min |

---

## 📞 Emergency Commands

```bash
# Kill stuck process
lsof -i :8000
kill -9 <PID>

# Reset everything
rm -rf venv db.sqlite3 gemma_validation/__pycache__

# View active processes
ps aux | grep python

# Monitor LLM
curl http://localhost:11434/api/tags

# View logs
tail -f run_server.py  # or use: less
```

---

**Last Updated**: May 2024  
**Status**: ✅ Ready to Use  
**Questions?** → See GETTING_STARTED.md
