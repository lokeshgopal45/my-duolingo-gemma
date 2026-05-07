package com.google.mediapipe.examples.llminference

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.google.mediapipe.examples.llminference.ui.JapanSenseiApp
import com.google.mediapipe.examples.llminference.ui.QuizViewModel
import com.google.mediapipe.examples.llminference.ui.theme.BgLight
import com.google.mediapipe.examples.llminference.ui.theme.LLMInferenceTheme

class MainActivity : ComponentActivity() {

    private val viewModel: QuizViewModel by viewModels {
        QuizViewModel.getFactory(this)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            LLMInferenceTheme {
                Scaffold { innerPadding ->
                    Surface(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(innerPadding),
                        color = BgLight,
                    ) {
                        JapanSenseiApp(viewModel)
                    }
                }
            }
        }
    }
}
