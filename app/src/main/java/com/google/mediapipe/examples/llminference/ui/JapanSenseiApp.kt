package com.google.mediapipe.examples.llminference.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.google.mediapipe.examples.llminference.ui.theme.*

data class LearningPath(
    val title: String,
    val description: String,
    val level: String,
)

@Composable
fun JapanSenseiApp(viewModel: QuizViewModel) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = BgLight
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    brush = Brush.radialGradient(
                        colors = listOf(
                            Color.White.copy(alpha = 0.92f),
                            Color.White.copy(alpha = 0.18f),
                            Color.Transparent
                        ),
                        radius = 600f
                    )
                )
        ) {
            when (val state = uiState) {
                is QuizUiState.Initial -> JapanWelcomeScreen(onEnter = { viewModel.generateLesson() })
                is QuizUiState.Loading -> JapanLoadingScreen()
                is QuizUiState.Error -> JapanErrorScreen(state.message, onRetry = { viewModel.generateLesson() })
                is QuizUiState.Quiz -> JapanQuizScreen(
                    question = state.questions[state.currentIndex],
                    currentIndex = state.currentIndex,
                    totalQuestions = state.questions.size,
                    streak = 0,
                    onAnswer = { isCorrect -> viewModel.answerQuestion(isCorrect) }
                )
                is QuizUiState.Results -> JapanResultsScreen(
                    score = state.score,
                    total = state.total,
                    onPlayAgain = { viewModel.playAgain() }
                )
            }
        }
    }
}

@Composable
fun JapanWelcomeScreen(onEnter: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(32.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.Start
    ) {
        // Brand badge
        Surface(
            modifier = Modifier
                .padding(bottom = 24.dp)
                .background(AccentSoft, shape = RoundedCornerShape(8.dp))
                .padding(horizontal = 12.dp, vertical = 6.dp),
            color = AccentSoft,
            shape = RoundedCornerShape(8.dp)
        ) {
            Text(
                text = "Japan Sensei",
                fontSize = 12.sp,
                fontWeight = FontWeight.SemiBold,
                color = AccentDark,
                letterSpacing = 0.5.sp
            )
        }

        Text(
            text = "Welcome to a calmer way to study Japanese.",
            fontSize = 36.sp,
            fontWeight = FontWeight.Bold,
            color = TextPrimary,
            lineHeight = 42.sp,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        Text(
            text = "A light, premium learning space for daily review, focused N3 practice, and quick confidence-building lessons.",
            fontSize = 16.sp,
            color = TextMuted,
            lineHeight = 24.sp,
            modifier = Modifier.padding(bottom = 32.dp)
        )

        // CTA Button
        Button(
            onClick = onEnter,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = AccentWarm),
            shape = RoundedCornerShape(14.dp)
        ) {
            Text(
                text = "Enter Japan Sensei",
                fontSize = 16.sp,
                fontWeight = FontWeight.SemiBold,
                color = Color.White
            )
        }
    }
}

@Composable
fun JapanLoadingScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        CircularProgressIndicator(
            color = AccentWarm,
            modifier = Modifier.size(48.dp)
        )
        Spacer(modifier = Modifier.height(20.dp))
        Text(
            text = "Loading your lesson...",
            fontSize = 16.sp,
            color = TextMuted,
            textAlign = TextAlign.Center
        )
    }
}

@Composable
fun JapanErrorScreen(message: String, onRetry: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Surface(
            modifier = Modifier
                .size(64.dp),
            shape = RoundedCornerShape(32.dp),
            color = DangerSoft
        ) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Text("!", fontSize = 32.sp, color = DangerRed, fontWeight = FontWeight.Bold)
            }
        }
        Spacer(modifier = Modifier.height(20.dp))
        Text(
            text = "Something went wrong",
            fontSize = 18.sp,
            fontWeight = FontWeight.SemiBold,
            color = TextPrimary
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = message,
            fontSize = 14.sp,
            color = TextMuted,
            textAlign = TextAlign.Center
        )
        Spacer(modifier = Modifier.height(32.dp))
        Button(
            onClick = onRetry,
            modifier = Modifier
                .fillMaxWidth()
                .height(48.dp),
            colors = ButtonDefaults.buttonColors(containerColor = AccentWarm),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text("Try Again", fontSize = 14.sp, color = Color.White, fontWeight = FontWeight.SemiBold)
        }
    }
}

@Composable
fun JapanQuizScreen(
    question: Question,
    currentIndex: Int,
    totalQuestions: Int,
    streak: Int,
    onAnswer: (Boolean) -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        // Header with progress
        Column {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 24.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Question ${currentIndex + 1} of $totalQuestions",
                    fontSize = 14.sp,
                    color = TextMuted,
                    fontWeight = FontWeight.Medium
                )
                Surface(
                    modifier = Modifier
                        .background(SuccessSoft, shape = RoundedCornerShape(8.dp))
                        .padding(horizontal = 10.dp, vertical = 4.dp),
                    color = SuccessSoft,
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text(
                        text = "Streak: $streak",
                        fontSize = 12.sp,
                        color = SuccessGreen,
                        fontWeight = FontWeight.SemiBold
                    )
                }
            }

            // Progress bar
            LinearProgressIndicator(
                progress = { (currentIndex + 1) / totalQuestions.toFloat() },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(4.dp),
                color = AccentWarm,
                trackColor = AccentSoft,
            )
        }

        // Question content
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f),
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = question.question,
                fontSize = 22.sp,
                fontWeight = FontWeight.SemiBold,
                color = TextPrimary,
                lineHeight = 32.sp,
                modifier = Modifier.padding(bottom = 24.dp)
            )

            if (question.options.isNotEmpty()) {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    for (option in question.options) {
                        Surface(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { onAnswer(option == question.correct_answer) }
                                .background(
                                    PanelGlass,
                                    shape = RoundedCornerShape(14.dp)
                                )
                                .padding(16.dp),
                            color = PanelGlass,
                            shape = RoundedCornerShape(14.dp)
                        ) {
                            Text(
                                text = option,
                                fontSize = 16.sp,
                                color = TextPrimary,
                                fontWeight = FontWeight.Medium
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun JapanResultsScreen(score: Int, total: Int, onPlayAgain: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Score badge
        Surface(
            modifier = Modifier
                .size(140.dp),
            shape = RoundedCornerShape(70.dp),
            color = AccentSoft
        ) {
            Column(
                modifier = Modifier.fillMaxSize(),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = "$score",
                    fontSize = 48.sp,
                    fontWeight = FontWeight.Bold,
                    color = AccentDark
                )
                Text(
                    text = "/ $total",
                    fontSize = 18.sp,
                    color = AccentWarm
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        val accuracy = ((score.toFloat() / total) * 100).toInt()
        Text(
            text = "Great work!",
            fontSize = 28.sp,
            fontWeight = FontWeight.Bold,
            color = TextPrimary
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "Accuracy: $accuracy%",
            fontSize = 16.sp,
            color = TextMuted
        )

        Spacer(modifier = Modifier.height(40.dp))

        Button(
            onClick = onPlayAgain,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = AccentWarm),
            shape = RoundedCornerShape(14.dp)
        ) {
            Text(
                text = "Try Another Lesson",
                fontSize = 16.sp,
                fontWeight = FontWeight.SemiBold,
                color = Color.White
            )
        }
    }
}
