package com.google.mediapipe.examples.llminference.ui

import kotlinx.serialization.Serializable

@Serializable
data class QuizResponse(
    val quiz: List<Question>
)

@Serializable
data class Question(
    val question: String,
    val options: List<String>,
    val correct_answer: String
)
