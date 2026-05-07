# Example API Requests

## Using Python Requests

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

# 1. Get all exercises
response = requests.get(f"{BASE_URL}/exercises/")
exercises = response.json()

# 2. Validate a single exercise
payload = {"exercise_id": 1}
response = requests.post(
    f"{BASE_URL}/results/validate_exercise/",
    json=payload
)
result = response.json()

print(f"Correct: {result['is_correct']}")
print(f"Confidence: {result['confidence_score']}")
print(f"Response: {result['gemma_response']}")

# 3. Batch validation
payload = {
    "exercise_ids": [1, 2, 3, 4, 5],
    "session_name": "Morning N3 Test"
}
response = requests.post(
    f"{BASE_URL}/results/validate_batch/",
    json=payload
)
batch_result = response.json()

print(f"Success Rate: {batch_result['summary']['success_rate']}%")

# 4. Get statistics
response = requests.get(f"{BASE_URL}/results/statistics/")
stats = response.json()

print(f"Total: {stats['total_validations']}")
print(f"Passed: {stats['passed']}")
print(f"By Type: {stats['by_exercise_type']}")
```

## Using cURL

```bash
# List all exercises
curl http://localhost:8000/api/exercises/ | jq

# Get exercise by type
curl "http://localhost:8000/api/exercises/by_type/?type=grammar" | jq

# Validate single exercise
curl -X POST http://localhost:8000/api/results/validate_exercise/ \
  -H "Content-Type: application/json" \
  -d '{
    "exercise_id": 1
  }' | jq

# Batch validation
curl -X POST http://localhost:8000/api/results/validate_batch/ \
  -H "Content-Type: application/json" \
  -d '{
    "exercise_ids": [1, 2, 3],
    "session_name": "Test Session"
  }' | jq

# Get statistics
curl http://localhost:8000/api/results/statistics/ | jq

# Create new exercise
curl -X POST http://localhost:8000/api/exercises/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "新しい問題",
    "exercise_type": "grammar",
    "jlpt_level": "N3",
    "prompt": "質問",
    "correct_answers": ["答え1", "答え2"],
    "explanation": "解説"
  }' | jq
```

## Using JavaScript/Node.js

```javascript
const BASE_URL = "http://localhost:8000/api";

// Validate exercise
async function validateExercise(exerciseId) {
  const response = await fetch(
    `${BASE_URL}/results/validate_exercise/`,
    {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({exercise_id: exerciseId})
    }
  );
  
  const result = await response.json();
  return result;
}

// Batch validation
async function batchValidate(exerciseIds) {
  const response = await fetch(
    `${BASE_URL}/results/validate_batch/`,
    {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        exercise_ids: exerciseIds,
        session_name: "JS Test"
      })
    }
  );
  
  const result = await response.json();
  console.log(`Success Rate: ${result.summary.success_rate}%`);
  return result;
}

// Get statistics
async function getStats() {
  const response = await fetch(`${BASE_URL}/results/statistics/`);
  return await response.json();
}

// Usage
validateExercise(1).then(console.log);
batchValidate([1, 2, 3]).then(console.log);
getStats().then(console.log);
```

## WebSocket Integration (Optional)

For real-time updates, you could add Django Channels:

```python
# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ValidationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        exercise_id = data['exercise_id']
        
        # Validate and send updates
        result = validate_exercise(exercise_id)
        
        await self.send(text_data=json.dumps({
            'status': 'complete',
            'result': result
        }))
```

Connect from frontend:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/validate/');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Validation complete:', data.result);
};

ws.send(JSON.stringify({exercise_id: 1}));
```
