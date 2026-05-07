package com.google.mediapipe.examples.llminference.ui

import android.content.Context
import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.google.mediapipe.examples.llminference.InferenceModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import java.io.File
import java.io.FileOutputStream

sealed class QuizUiState {
    object Loading : QuizUiState()
    object Initial : QuizUiState()
    data class Error(val message: String) : QuizUiState()
    data class Quiz(val questions: List<Question>, val currentIndex: Int, val score: Int) : QuizUiState()
    data class Results(val score: Int, val total: Int) : QuizUiState()
}

class QuizViewModel(private val inferenceModel: InferenceModel) : ViewModel() {

    private val _uiState = MutableStateFlow<QuizUiState>(QuizUiState.Initial)
    val uiState: StateFlow<QuizUiState> = _uiState.asStateFlow()

    private val prompt = """
        You are a Japanese language quiz generator. Generate a 3-question multiple-choice quiz targeting JLPT N3 vocabulary and grammar. You must output ONLY a raw, valid JSON object and absolutely no markdown or conversational text. The JSON format must be: {"quiz": [{"question": "Translate: [English phrase]", "options": ["Option A", "Option B", "Option C", "Option D"], "correct_answer": "Option B"}]}.
    """.trimIndent()

    private val jsonParser = Json { ignoreUnknownKeys = true }

    fun generateLesson() {
        _uiState.value = QuizUiState.Loading
        viewModelScope.launch(Dispatchers.IO) {
            try {
                // Initialize model session if needed
                // For simplicity, generate response
                val responseFuture = inferenceModel.generateResponseAsync(prompt) { partial, done ->
                    // We don't necessarily need to track partial tokens for this, 
                    // since we need valid JSON at the end.
                }
                
                val rawResponse = responseFuture.get() // Block until future completes
                
                // Clean markdown from response
                val cleanJson = rawResponse
                    .replace("```json", "")
                    .replace("```", "")
                    .trim()

                Log.d("QuizViewModel", "Parsed JSON: ${cleanJson}")
                
                val quizResponse = jsonParser.decodeFromString<QuizResponse>(cleanJson)
                
                launch(Dispatchers.Main) {
                    if (quizResponse.quiz.isNotEmpty()) {
                        _uiState.value = QuizUiState.Quiz(quizResponse.quiz, 0, 0)
                    } else {
                        _uiState.value = QuizUiState.Error("No questions generated.")
                    }
                }
            } catch (e: Exception) {
                Log.e("QuizViewModel", "Error generating lesson", e)
                launch(Dispatchers.Main) {
                    _uiState.value = QuizUiState.Error("Failed to generate quiz: ${e.localizedMessage}")
                }
            }
        }
    }

    fun answerQuestion(isCorrect: Boolean) {
        val currentState = _uiState.value
        if (currentState is QuizUiState.Quiz) {
            val newScore = if (isCorrect) currentState.score + 1 else currentState.score
            val nextIndex = currentState.currentIndex + 1
            
            if (nextIndex < currentState.questions.size) {
                _uiState.value = currentState.copy(currentIndex = nextIndex, score = newScore)
            } else {
                _uiState.value = QuizUiState.Results(newScore, currentState.questions.size)
            }
        }
    }

    fun playAgain() {
        _uiState.value = QuizUiState.Initial
    }

    override fun onCleared() {
        super.onCleared()
        inferenceModel.close()
    }

    companion object {
        fun getFactory(context: Context) = object : ViewModelProvider.Factory {
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                // Here we initialize the InferenceModel
                // We will copy the asset to internal storage first
                val modelFile = copyAssetToInternalStorage(context, "gemma-4-e2b.task")
                
                // Set the inference model path to point to our extracted file
                InferenceModel.modelPathOverride = modelFile.absolutePath
                val inferenceModel = InferenceModel.getInstance(context)
                
                @Suppress("UNCHECKED_CAST")
                return QuizViewModel(inferenceModel) as T
            }
        }
        
        private fun copyAssetToInternalStorage(context: Context, assetName: String): File {
            val file = File(context.filesDir, assetName)
            if (!file.exists()) {
                try {
                    context.assets.open(assetName).use { inputStream ->
                        FileOutputStream(file).use { outputStream ->
                            inputStream.copyTo(outputStream)
                        }
                    }
                } catch (e: Exception) {
                    Log.e("QuizViewModel", "Error copying asset", e)
                }
            }
            return file
        }
    }
}
