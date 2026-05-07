import React, { useEffect, useState } from 'react'
import { quizPlaygrounds, validateChoiceWithGemma } from './quizBank'

const heroStats = [
  { label: 'Playgrounds', value: '4 modes' },
  { label: 'Questions', value: '60 total' },
  { label: 'Per mode', value: '15 questions' },
  { label: 'Validation', value: 'Gemma E2B' },
]

function WelcomeScreen({ onEnter }) {
  return (
    <div className="welcome-shell card">
      <div className="welcome-copy">
        <span className="brand-badge">Japan Sensei</span>
        <h1>Four study playgrounds, one calm practice flow.</h1>
        <p className="hero-text">
          Switch between Text, Audio, Writing, and Listening. Every answer is checked against the local Gemma E2B model so the result stays grounded.
        </p>
        <div className="hero-actions">
          <button className="primary" onClick={onEnter}>Enter Japan Sensei</button>
        </div>
      </div>

      <div className="welcome-preview">
        <div className="preview card soft-panel">
          <div className="preview-top">
            <span>Practice mode</span>
            <span className="status-pill">4 playgrounds</span>
          </div>
          <h2>Pick a mode, answer 15 questions, and review with Gemma.</h2>
          <p>
            This version keeps the interface light while making the validation path real.
          </p>
        </div>

        <div className="stat-grid">
          {heroStats.map((item) => (
            <div key={item.label} className="stat-card">
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function ModeSelectionScreen({ onSelectMode }) {
  return (
    <div className="mode-shell">
      <section className="card mode-hero">
        <span className="brand-badge">Japan Sensei</span>
        <h1>Choose a playground.</h1>
        <p className="hero-text">
          Each playground has 15 questions. Text and Writing focus on form, while Audio and Listening lean on spoken cues.
        </p>
        <div className="stat-grid mode-stats">
          {heroStats.map((item) => (
            <div key={item.label} className="stat-card">
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="mode-grid">
        {quizPlaygrounds.map((mode) => (
          <article key={mode.id} className="mode-card card">
            <div className="mode-card-top">
              <span className="status-pill">15 questions</span>
              <span className="brand-chip">Gemma cross-check</span>
            </div>
            <div>
              <p className="eyebrow">{mode.hint}</p>
              <h2>{mode.title}</h2>
            </div>
            <p>{mode.description}</p>
            <button className="primary mode-action" onClick={() => onSelectMode(mode.id)}>
              Start {mode.title}
            </button>
          </article>
        ))}
      </section>
    </div>
  )
}

function LoadingScreen() {
  return (
    <div className="screen card loading-screen">
      <div className="spinner" />
      <h2>Preparing the playground...</h2>
      <p>Japan Sensei is loading the quiz set and model validation flow.</p>
    </div>
  )
}

function ErrorScreen({ message, onRetry }) {
  return (
    <div className="screen card error-screen">
      <span className="status-pill danger">Session error</span>
      <h2>Something interrupted the playground.</h2>
      <p>{message}</p>
      <button className="primary" onClick={onRetry}>Try again</button>
    </div>
  )
}

function QuizScreen({ playground, question, currentIndex, totalQuestions, onSubmitAnswer, onAdvance, streak }) {
  const [selected, setSelected] = useState(null)
  const [validation, setValidation] = useState(null)
  const [showResult, setShowResult] = useState(false)
  const [isChecking, setIsChecking] = useState(false)

  useEffect(() => {
    setSelected(null)
    setValidation(null)
    setShowResult(false)
    setIsChecking(false)
  }, [question.question])

  const handlePlayCue = () => {
    if (!question.audioCue || typeof window === 'undefined' || !window.speechSynthesis) {
      return
    }

    const utterance = new SpeechSynthesisUtterance(question.audioCue)
    utterance.lang = 'ja-JP'
    window.speechSynthesis.cancel()
    window.speechSynthesis.speak(utterance)
  }

  const handleCheck = async () => {
    if (!selected || isChecking) {
      return
    }

    setIsChecking(true)
    try {
      const result = await onSubmitAnswer(question, selected)
      setValidation(result)
      setShowResult(true)
    } finally {
      setIsChecking(false)
    }
  }

  const handleNext = () => {
    if (validation) {
      onAdvance(validation)
    }
  }

  const selectedClass = (option) => (selected === option ? 'selected' : '')
  const correctClass = (option) => showResult && validation?.correct_answer === option ? 'correct' : ''
  const wrongClass = (option) => showResult && selected === option && validation?.correct_answer !== option ? 'wrong' : ''

  return (
    <div className="quiz-layout">
      <aside className="quiz-rail card">
        <div className="rail-head">
          <span className="brand-badge small">Japan Sensei</span>
          <span className="status-pill">Streak {streak} days</span>
        </div>
        <div className="rail-progress">
          <span>{playground.title}</span>
          <strong>{currentIndex + 1} / {totalQuestions}</strong>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: `${((currentIndex + 1) / totalQuestions) * 100}%` }} />
          </div>
        </div>
        <div className="rail-note">
          <p className="eyebrow">Mode focus</p>
          <p>{playground.hint}</p>
          <p>Read once, choose once, then let Gemma confirm the result.</p>
        </div>
      </aside>

      <main className="quiz-main card">
        <div className="quiz-head">
          <div>
            <span className="eyebrow">{playground.title}</span>
            <h2>{question.question}</h2>
          </div>
          <span className="status-pill subtle">Question {currentIndex + 1}</span>
        </div>

        {question.audioCue && (
          <div className="audio-banner card soft-panel">
            <div>
              <p className="eyebrow">Audio cue</p>
              <strong>{question.audioCue}</strong>
            </div>
            <button className="secondary" onClick={handlePlayCue}>Play audio cue</button>
          </div>
        )}

        <div className="option-grid">
          {question.options.map((option, index) => (
            <button
              key={option}
              className={`option-card ${selectedClass(option)} ${correctClass(option)} ${wrongClass(option)}`.trim()}
              onClick={() => !showResult && setSelected(option)}
              disabled={showResult}
            >
              <span className="option-index">0{index + 1}</span>
              <span>{option}</span>
            </button>
          ))}
        </div>

        {showResult && validation && (
          <div className={`answer-panel ${validation.is_correct ? 'correct' : 'wrong'}`}>
            <div>
              <p className="eyebrow">Gemma cross-check</p>
              <h3>{validation.is_correct ? 'Correct choice.' : 'Not quite.'}</h3>
            </div>
            <p>
              Gemma chose <strong>{validation.gemma_answer || 'an unclear answer'}</strong>. The reference answer is <strong>{validation.correct_answer}</strong>.
            </p>
            <p>{validation.validation_notes}</p>
          </div>
        )}

        <div className="quiz-actions">
          {!showResult && (
            <button className="primary" onClick={handleCheck} disabled={!selected || isChecking}>
              {isChecking ? 'Checking with Gemma...' : 'Check answer'}
            </button>
          )}

          {showResult && (
            <button className="primary" onClick={handleNext}>
              {currentIndex === totalQuestions - 1 ? 'Finish playground' : 'Next question'}
            </button>
          )}
        </div>
      </main>
    </div>
  )
}

function ResultsScreen({ playground, score, total, gemmaMatches, onPlayAgain }) {
  const accuracy = Math.round((score / total) * 100)

  return (
    <div className="results-shell card">
      <span className="status-pill success">{playground.title} complete</span>
      <h1>Strong session with Japan Sensei.</h1>
      <p className="hero-text">You kept the pace steady and finished the full 15-question playground.</p>

      <div className="results-metric">
        <div>
          <span>Score</span>
          <strong>{score} / {total}</strong>
        </div>
        <div>
          <span>Accuracy</span>
          <strong>{accuracy}%</strong>
        </div>
      </div>

      <div className="results-metric">
        <div>
          <span>Gemma agreement</span>
          <strong>{gemmaMatches} / {total}</strong>
        </div>
        <div>
          <span>Mode</span>
          <strong>{playground.title}</strong>
        </div>
      </div>

      <div className="results-tips">
        <article>
          <h3>Next step</h3>
          <p>Try another playground and compare how the pattern changes between reading, listening, and writing.</p>
        </article>
        <article>
          <h3>Momentum</h3>
          <p>Keep the session short and repeat one more mode while the answers are still fresh.</p>
        </article>
      </div>

      <div className="hero-actions">
        <button className="primary" onClick={onPlayAgain}>Choose another playground</button>
      </div>
    </div>
  )
}

export default function App() {
  const [state, setState] = useState('welcome')
  const [activeModeId, setActiveModeId] = useState(null)
  const [questions, setQuestions] = useState([])
  const [index, setIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [gemmaMatches, setGemmaMatches] = useState(0)
  const [error, setError] = useState('')
  const [streak] = useState(0)

  useEffect(() => {
    document.title = 'Japan Sensei'
  }, [])

  const activePlayground = quizPlaygrounds.find((mode) => mode.id === activeModeId) || null

  const enterApp = () => {
    setState('modes')
  }

  const startMode = (modeId) => {
    const nextMode = quizPlaygrounds.find((mode) => mode.id === modeId)
    if (!nextMode) {
      setError('The selected playground could not be loaded.')
      setState('error')
      return
    }

    setActiveModeId(modeId)
    setQuestions(nextMode.questions)
    setIndex(0)
    setScore(0)
    setGemmaMatches(0)
    setState('quiz')
  }

  const handleSubmitAnswer = async (question, selectedAnswer) => {
    if (!activePlayground) {
      throw new Error('No playground is active.')
    }

    return validateChoiceWithGemma({
      playground: activePlayground,
      question,
      selectedAnswer,
    })
  }

  const handleAdvance = (validation) => {
    if (validation?.is_correct) {
      setScore((current) => current + 1)
    }

    if (validation?.gemma_agrees) {
      setGemmaMatches((current) => current + 1)
    }

    const nextIndex = index + 1
    if (nextIndex < questions.length) {
      setIndex(nextIndex)
    } else {
      setState('results')
    }
  }

  const playAgain = () => {
    setState('modes')
    setActiveModeId(null)
    setQuestions([])
    setIndex(0)
    setScore(0)
    setGemmaMatches(0)
  }

  const topbarText =
    state === 'welcome'
      ? 'A calmer way to study Japanese.'
      : activePlayground
        ? `Active mode: ${activePlayground.title}`
        : 'Choose a playground to begin.'

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <span className="brand-badge">Japan Sensei</span>
          <p>{topbarText}</p>
        </div>
        <div className="topbar-metrics">
          <span>Mode <strong>{activePlayground ? activePlayground.title : 'Ready'}</strong></span>
          <span>Playgrounds <strong>4</strong></span>
          <span>Gemma <strong>{gemmaMatches} checks</strong></span>
        </div>
      </header>

      {state === 'welcome' && <WelcomeScreen onEnter={enterApp} />}
      {state === 'modes' && <ModeSelectionScreen onSelectMode={startMode} />}
      {state === 'quiz' && activePlayground && questions[index] && (
        <QuizScreen
          playground={activePlayground}
          question={questions[index]}
          currentIndex={index}
          totalQuestions={questions.length}
          onSubmitAnswer={handleSubmitAnswer}
          onAdvance={handleAdvance}
          streak={streak}
        />
      )}
      {state === 'results' && activePlayground && (
        <ResultsScreen
          playground={activePlayground}
          score={score}
          total={questions.length}
          gemmaMatches={gemmaMatches}
          onPlayAgain={playAgain}
        />
      )}
      {state === 'error' && <ErrorScreen message={error} onRetry={playAgain} />}
    </div>
  )
}
