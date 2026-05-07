package com.google.mediapipe.examples.llminference.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@Composable
fun QuizApp(viewModel: QuizViewModel) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = Color(0xFFF0F4F8) // Soft gray background
    ) {
        when (val state = uiState) {
            is QuizUiState.Initial -> InitialScreen(onStart = { viewModel.generateLesson() })
            is QuizUiState.Loading -> LoadingScreen()
            is QuizUiState.Error -> ErrorScreen(state.message, onRetry = { viewModel.generateLesson() })
            is QuizUiState.Quiz -> QuizScreen(
                question = state.questions[state.currentIndex],
                currentIndex = state.currentIndex,
                totalQuestions = state.questions.size,
                onAnswer = { viewModel.answerQuestion(it) }
            )
            is QuizUiState.Results -> ResultsScreen(
                score = state.score,
                total = state.total,
                onPlayAgain = { viewModel.playAgain() }
            )
        }
    }
}

@Composable
fun InitialScreen(onStart: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Japanese N3 Quiz",
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF2D3748)
        )
        Spacer(modifier = Modifier.height(32.dp))
        Button(
            onClick = onStart,
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50)),
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier.height(56.dp).padding(horizontal = 32.dp)
        ) {
            Text("Generate Lesson", fontSize = 18.sp, color = Color.White)
        }
    }
}

@Composable
fun LoadingScreen() {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        CircularProgressIndicator(color = Color(0xFF4CAF50))
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = "Generating Lesson...",
            fontSize = 18.sp,
            color = Color(0xFF4A5568)
        )
    }
}

@Composable
fun ErrorScreen(message: String, onRetry: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize().padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Oops!",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFFE53E3E)
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = message,
            textAlign = TextAlign.Center,
            color = Color(0xFF4A5568)
        )
        Spacer(modifier = Modifier.height(32.dp))
        Button(
            onClick = onRetry,
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50))
        ) {
            Text("Try Again")
        }
    }
}

@Composable
fun QuizScreen(
    question: Question,
    currentIndex: Int,
    totalQuestions: Int,
    onAnswer: (Boolean) -> Unit
) {
    var selectedOption by remember { mutableStateOf<String?>(null) }
    var showResult by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Question ${currentIndex + 1} of $totalQuestions",
            fontSize = 16.sp,
            color = Color(0xFF718096),
            modifier = Modifier.padding(top = 32.dp, bottom = 16.dp)
        )
        
        Text(
            text = question.question,
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF2D3748),
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(bottom = 32.dp)
        )

        question.options.forEach { option ->
            val isSelected = selectedOption == option
            val isCorrect = option == question.correct_answer
            
            val backgroundColor = when {
                !showResult -> Color.White
                isCorrect -> Color(0xFFC6F6D5) // Green for correct
                isSelected && !isCorrect -> Color(0xFFFED7D7) // Red for wrong selected
                else -> Color.White
            }
            
            val borderColor = when {
                !showResult -> Color(0xFFE2E8F0)
                isCorrect -> Color(0xFF48BB78)
                isSelected && !isCorrect -> Color(0xFFF56565)
                else -> Color(0xFFE2E8F0)
            }

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp)
                    .background(backgroundColor, RoundedCornerShape(12.dp))
                    .clickable(enabled = !showResult) {
                        selectedOption = option
                    }
                    .padding(16.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = option,
                    fontSize = 18.sp,
                    color = Color(0xFF2D3748)
                )
            }
        }

        Spacer(modifier = Modifier.weight(1f))

        if (selectedOption != null && !showResult) {
            Button(
                onClick = { showResult = true },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50)),
                modifier = Modifier.fillMaxWidth().height(56.dp),
                shape = RoundedCornerShape(16.dp)
            ) {
                Text("Check Answer", fontSize = 18.sp)
            }
        } else if (showResult) {
            Button(
                onClick = { 
                    onAnswer(selectedOption == question.correct_answer)
                    selectedOption = null
                    showResult = false
                },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50)),
                modifier = Modifier.fillMaxWidth().height(56.dp),
                shape = RoundedCornerShape(16.dp)
            ) {
                Text(if (currentIndex == totalQuestions - 1) "Finish" else "Next", fontSize = 18.sp)
            }
        }
    }
}

@Composable
fun ResultsScreen(score: Int, total: Int, onPlayAgain: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Quiz Complete!",
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF2D3748)
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = "You scored",
            fontSize = 20.sp,
            color = Color(0xFF718096)
        )
        Text(
            text = "$score / $total",
            fontSize = 48.sp,
            fontWeight = FontWeight.ExtraBold,
            color = Color(0xFF4CAF50)
        )
        Spacer(modifier = Modifier.height(48.dp))
        Button(
            onClick = onPlayAgain,
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF3182CE)),
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier.height(56.dp).padding(horizontal = 32.dp)
        ) {
            Text("Play Again", fontSize = 18.sp, color = Color.White)
        }
    }
}
