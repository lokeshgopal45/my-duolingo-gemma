"""
LLM Integration utilities for Ollama and LM Studio
"""
import requests
import json
import time
import logging
from typing import Dict, Tuple
from django.conf import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Base client for LLM interaction"""
    
    def __init__(self, provider: str, base_url: str, model: str, timeout: int = 120):
        self.provider = provider
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
    
    @staticmethod
    def from_settings():
        """Create client from Django settings"""
        return LLMClient(
            provider=settings.LLM_PROVIDER,
            base_url=settings.LLM_BASE_URL,
            model=settings.LLM_MODEL,
            timeout=settings.LLM_TIMEOUT
        )
    
    def is_available(self) -> bool:
        """Check if LLM service is running"""
        try:
            if self.provider == 'ollama':
                response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            elif self.provider == 'lm_studio':
                response = requests.get(f"{self.base_url}/v1/models", timeout=5)
            else:
                return False
            return response.status_code == 200
        except Exception as e:
            logger.error(f"LLM service check failed: {e}")
            return False
    
    def query(self, prompt: str, temperature: float = 0.7) -> Tuple[str, Dict]:
        """Send query to LLM and get response"""
        start_time = time.time()
        
        try:
            if self.provider == 'ollama':
                response = self._query_ollama(prompt, temperature)
            elif self.provider == 'lm_studio':
                response = self._query_lm_studio(prompt, temperature)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
            
            elapsed_ms = int((time.time() - start_time) * 1000)
            
            return response, {
                'elapsed_ms': elapsed_ms,
                'provider': self.provider,
                'model': self.model
            }
        except Exception as e:
            logger.error(f"LLM query failed: {e}")
            raise
    
    def _query_ollama(self, prompt: str, temperature: float) -> str:
        """Query Ollama API"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False,
        }
        
        response = requests.post(
            url,
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        return result.get('response', '').strip()
    
    def _query_lm_studio(self, prompt: str, temperature: float) -> str:
        """Query LM Studio OpenAI-compatible API"""
        url = f"{self.base_url}/v1/completions"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": 512,
        }
        
        response = requests.post(
            url,
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['text'].strip()


class JapaneseExerciseValidator:
    """Validate Gemma responses for Japanese N3 exercises"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
    
    def build_exercise_prompt(self, exercise) -> str:
        """Build prompt for the LLM based on exercise type"""
        
        if exercise.exercise_type == 'reading':
            prompt = f"""与えられた文章を読んで、以下の質問に答えてください。

文章：
{exercise.context}

質問：
{exercise.prompt}

簡潔に答えてください。"""
        
        elif exercise.exercise_type == 'grammar':
            prompt = f"""以下の文法問題に答えてください。

質問：
{exercise.prompt}

選択肢または文を完成させてください。"""
        
        elif exercise.exercise_type == 'vocabulary':
            prompt = f"""以下の語彙問題に答えてください。

質問：
{exercise.prompt}

最も適切な答えを選んでください。"""
        
        elif exercise.exercise_type == 'kanji':
            prompt = f"""以下の漢字問題に答えてください。

質問：
{exercise.prompt}

読み方または意味を答えてください。"""
        
        else:
            prompt = exercise.prompt
        
        return prompt
    
    def validate_response(self, 
                         exercise,
                         gemma_response: str) -> Tuple[bool, float, str]:
        """
        Validate Gemma's response against correct answers
        Returns: (is_correct, confidence_score, notes)
        """
        
        correct_answers = exercise.correct_answers
        response_lower = gemma_response.lower().strip()
        
        # Check for exact matches (Japanese and romanized)
        for answer in correct_answers:
            if isinstance(answer, dict):
                # Handle multi-field answers
                for field, value in answer.items():
                    if value.lower() in response_lower or value in gemma_response:
                        return True, 0.95, "Exact match found"
            else:
                # Simple string comparison
                answer_lower = str(answer).lower()
                if answer_lower in response_lower or answer_lower == response_lower:
                    return True, 0.9, "Exact match found"
        
        # Use LLM to verify semantic correctness
        verification_result = self._verify_with_llm(
            exercise,
            gemma_response,
            correct_answers
        )
        
        return verification_result
    
    def _verify_with_llm(self, exercise, response: str, correct_answers: list) -> Tuple[bool, float, str]:
        """Use LLM to verify semantic correctness"""
        
        answers_text = "\n".join([str(a) for a in correct_answers])
        
        verification_prompt = f"""以下の問題と答えを評価してください。

問題：
{exercise.prompt}

正解例：
{answers_text}

学生の答え：
{response}

この答えが正解である確率を評価してください（0-100）。
理由も簡潔に説明してください。

形式：
確率: [数字]%
理由: [説明]"""
        
        try:
            llm_eval, metadata = self.llm_client.query(verification_prompt, temperature=0.3)
            
            # Parse LLM evaluation
            lines = llm_eval.split('\n')
            probability = 0.5  # Default
            reason = "LLM evaluation performed"
            
            for line in lines:
                if '確率' in line or 'Rate' in line or '%' in line:
                    try:
                        prob_str = ''.join(filter(str.isdigit, line))
                        if prob_str:
                            probability = int(prob_str) / 100
                    except:
                        pass
                if '理由' in line or 'Reason' in line:
                    reason = line.replace('理由:', '').replace('Reason:', '').strip()
            
            is_correct = probability >= 0.7
            
            return is_correct, probability, reason
            
        except Exception as e:
            logger.error(f"LLM verification failed: {e}")
            # Fall back to keyword matching
            keywords = [a.split()[0] if isinstance(a, str) else str(a) for a in correct_answers]
            keyword_found = any(kw.lower() in response.lower() for kw in keywords)
            
            return keyword_found, 0.5, f"Fallback verification: keyword matching"
