import React, { useEffect, useState } from 'react'
import { generateQuiz } from './mockModel'

const quickStats = [
  { label: 'Streak', value: '0 days' },
  { label: 'Lessons', value: '28' },
  { label: 'Accuracy', value: '92%' },
  { label: 'Saved', value: '14 cards' },
]

const featureCards = [
  {
    eyebrow: 'Guided flow',
    title: 'Micro-lessons that feel calm and premium.',
    description:
      'A clean learning path with just enough structure to keep momentum without visual noise.',
  },
  {
    eyebrow: 'Smart practice',
    title: 'Quiz mode built around active recall.',
    description:
      'Tap through exercises, check answers instantly, and review the correct response with confidence.',
  },
  {
    eyebrow: 'Progress tracking',
    title: 'See streaks, mastery, and completion at a glance.',
    description:
      'A lightweight dashboard keeps the experience motivating while staying easy on the eyes.',
  },
]

const learningPaths = [
  {
    title: 'Starter Pack',
    description: 'Fast wins for greetings, particles, and common phrases.',
    level: 'Beginner-friendly',
  },
  {
    title: 'N3 Sprint',
    description: 'Reading, grammar, and vocabulary drills tuned for JLPT N3.',
    level: 'Focused practice',
  },
  {
    title: 'Daily Recall',
    description: 'Short reviews that keep your streak warm without overload.',
    level: '5 min refresh',
  },
]

function WelcomeScreen({ onEnter }) {
  return (
    <div className="welcome-shell card">
      <div className="welcome-copy">
        <span className="brand-badge">Japan Sensei</span>
        <h1>Welcome to a calmer way to study Japanese.</h1>
        <p className="hero-text">
          A light, premium learning space for daily review, focused N3 practice, and quick confidence-building lessons.
        </p>
        <div className="hero-actions">
          <button className="primary" onClick={onEnter}>Enter Japan Sensei</button>
        </div>
      </div>


    </div>
  )
}

function InitialScreen({ onStart, onExplore }) {
  return (
    <div className="hero-shell">
      <section className="hero-copy card">
        <div className="brand-row">
          <span className="brand-badge">Japan Sensei</span>
          <span className="brand-chip">Light premium learning</span>
        </div>
        <h1>Learn Japanese with a calmer, more polished study flow.</h1>
        <p className="hero-text">
          Japan Sensei blends guided lessons, instant quiz feedback, and a distraction-free interface for daily language practice.
        </p>
        <div className="hero-actions">
          <button className="primary" onClick={onStart}>Start a lesson</button>
          <button className="secondary ghost" onClick={onExplore}>Explore the dashboard</button>
        </div>
        <div className="stat-grid">
          {quickStats.map((item) => (
            <div key={item.label} className="stat-card">
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </div>
          ))}
        </div>
      </section>

      <aside className="hero-side">
        <div className="preview card">
          <div className="preview-top">
            <span>Today’s focus</span>
            <span className="status-pill">N3 practice</span>
          </div>
          <h2>Polite language and everyday school phrases.</h2>
          <p>
            A premium learning app layout with calm spacing, soft shadows, and clear progress cues.
          </p>
          <div className="mini-meter">
            <div className="mini-meter-fill" />
          </div>
          <div className="mini-meter-row">
            <span>Lesson completion</span>
            <strong>68%</strong>
          </div>
        </div>

        <div className="path-list card">
          <div className="section-title">
            <span>Study paths</span>
            <p>Pick a mode that matches your energy today.</p>
          </div>
          <div className="paths">
            {learningPaths.map((path) => (
              <article key={path.title} className="path-card">
                <div>
                  <span className="path-level">{path.level}</span>
                  <h3>{path.title}</h3>
                </div>
                <p>{path.description}</p>
              </article>
            ))}
          </div>
        </div>
      </aside>
    </div>
  )
}

function LoadingScreen() {
  return (
    <div className="screen card loading-screen">
      <div className="spinner" />
      <h2>Building your lesson...</h2>
      <p>Japan Sensei is preparing a short, focused practice set for you.</p>
    </div>
  )
}

function ErrorScreen({ message, onRetry }) {
  return (
    <div className="screen card error-screen">
      <span className="status-pill danger">Lesson unavailable</span>
      <h2>Something interrupted the lesson flow.</h2>
      <p>{message}</p>
      <button className="primary" onClick={onRetry}>Try again</button>
    </div>
  )
}

function QuizScreen({ question, currentIndex, totalQuestions, onAnswer, streak }) {
  const [selected, setSelected] = useState(null)
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)

  const handleCheck = () => {
    const correct = selected === question.correct_answer
    setIsCorrect(correct)
    setShowResult(true)
  }

  const handleNext = () => {
    onAnswer(isCorrect)
    setSelected(null)
    setShowResult(false)
    setIsCorrect(false)
  }

  return (
    <div className="quiz-layout">
      <aside className="quiz-rail card">
        <div className="rail-head">
          <span className="brand-badge small">Japan Sensei</span>
          <span className="status-pill">Streak {streak} days</span>
        </div>
        <div className="rail-progress">
          <span>Lesson progress</span>
          <strong>{currentIndex + 1} / {totalQuestions}</strong>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: `${((currentIndex + 1) / totalQuestions) * 100}%` }} />
          </div>
        </div>
        <div className="rail-note">
          <p className="eyebrow">Focus tip</p>
          <p>Read the prompt once, then trust your first instinct before checking the answer.</p>
        </div>
      </aside>

      <main className="quiz-main card">
        <div className="quiz-head">
          <div>
            <span className="eyebrow">Daily lesson</span>
            <h2>{question.question}</h2>
          </div>
          <span className="status-pill subtle">Question {currentIndex + 1}</span>
        </div>

        <div className="option-grid">
          {question.options.map((opt, index) => {
            const selectedClass = selected === opt ? 'selected' : ''
            const correctClass = showResult && opt === question.correct_answer ? 'correct' : ''
            const wrongClass = showResult && selected === opt && opt !== question.correct_answer ? 'wrong' : ''

            return (
              <button
                key={opt}
                className={`option-card ${selectedClass} ${correctClass} ${wrongClass}`.trim()}
                onClick={() => !showResult && setSelected(opt)}
              >
                <span className="option-index">0{index + 1}</span>
                <span>{opt}</span>
              </button>
            )
          })}
        </div>

        {showResult && (
          <div className={`answer-panel ${isCorrect ? 'correct' : 'wrong'}`}>
            <div>
              <p className="eyebrow">Answer review</p>
              <h3>{isCorrect ? 'Nice work.' : 'Almost there.'}</h3>
            </div>
            <p>
              {isCorrect
                ? 'That choice matches the intended meaning perfectly.'
                : `The correct answer is ${question.correct_answer}.`}
            </p>
          </div>
        )}

        <div className="quiz-actions">
          {!showResult && (
            <button className="primary" onClick={handleCheck} disabled={!selected}>
              Check answer
            </button>
          )}

          {showResult && (
            <button className="primary" onClick={handleNext}>
              {currentIndex === totalQuestions - 1 ? 'Finish lesson' : 'Next question'}
            </button>
          )}
        </div>
      </main>
    </div>
  )
}

function ResultsScreen({ score, total, onPlayAgain }) {
  const accuracy = Math.round((score / total) * 100)

  return (
    <div className="results-shell card">
      <span className="status-pill success">Lesson complete</span>
      <h1>Strong session with Japan Sensei.</h1>
      <p className="hero-text">You kept the pace steady and completed the lesson with a clear result.</p>

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

      <div className="results-tips">
        <article>
          <h3>Next step</h3>
          <p>Review the missed question once, then try one more short lesson to lock it in.</p>
        </article>
        <article>
          <h3>Momentum</h3>
          <p>Keep your streak alive with a short daily session rather than a long study block.</p>
        </article>
      </div>

      <div className="hero-actions">
        <button className="primary" onClick={onPlayAgain}>Study again</button>
        <button className="secondary ghost" onClick={onPlayAgain}>Back to dashboard</button>
      </div>
    </div>
  )
}

export default function App() {
  const [state, setState] = useState('welcome') // welcome, initial, loading, quiz, results, error
  const [quiz, setQuiz] = useState(null)
  const [index, setIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [error, setError] = useState('')
  const [streak, setStreak] = useState(0)

  useEffect(() => {
    document.title = 'Japan Sensei'
  }, [])

  const start = async () => {
    setState('loading')
    try {
      const resp = await generateQuiz()
      if (resp && resp.quiz && resp.quiz.length) {
        setQuiz(resp.quiz)
        setIndex(0)
        setScore(0)
        setState('quiz')
      } else {
        setError('No questions generated.')
        setState('error')
      }
    } catch (e) {
      setError('Failed to generate quiz')
      setState('error')
    }
  }

  const handleAnswer = (isCorrect) => {
    if (isCorrect) setScore((s) => s + 1)
    const next = index + 1
    if (next < quiz.length) {
      setIndex(next)
    } else {
      setState('results')
    }
  }

  const playAgain = () => {
    setState('initial')
    setQuiz(null)
    setIndex(0)
    setScore(0)
  }

  const exploreDashboard = () => {
    const target = document.getElementById('feature-grid')
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div />
      </header>

      {state === 'welcome' && <WelcomeScreen onEnter={() => setState('initial')} />}
      {state === 'initial' && <InitialScreen onStart={start} onExplore={exploreDashboard} />}
      {state === 'loading' && <LoadingScreen />}
      {state === 'error' && <ErrorScreen message={error} onRetry={start} />}
      {state === 'quiz' && quiz && (
        <QuizScreen
          question={quiz[index]}
          currentIndex={index}
          totalQuestions={quiz.length}
          onAnswer={handleAnswer}
          streak={streak}
        />
      )}
      {state === 'results' && <ResultsScreen score={score} total={quiz.length} onPlayAgain={playAgain} />}

      {state === 'initial' && (
        <section id="feature-grid" className="feature-grid">
          {featureCards.map((feature) => (
            <article key={feature.title} className="feature-card card">
              <span className="eyebrow">{feature.eyebrow}</span>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </article>
          ))}
        </section>
      )}
    </div>
  )
}
