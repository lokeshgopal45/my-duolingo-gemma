import React, { useState } from 'react'
import { generateQuiz } from './mockModel'

function InitialScreen({ onStart }) {
  return (
    <div className="center">
      <h1>Japanese N3 Quiz</h1>
      <button className="primary" onClick={onStart}>Generate Lesson</button>
    </div>
  )
}

function LoadingScreen() {
  return (
    <div className="center">
      <div className="spinner" />
      <p>Generating Lesson...</p>
    </div>
  )
}

function ErrorScreen({ message, onRetry }) {
  return (
    <div className="center">
      <h2>Oops!</h2>
      <p>{message}</p>
      <button onClick={onRetry}>Try Again</button>
    </div>
  )
}

function QuizScreen({ question, currentIndex, totalQuestions, onAnswer }) {
  const [selected, setSelected] = useState(null)
  const [showResult, setShowResult] = useState(false)

  return (
    <div className="container">
      <p className="meta">Question {currentIndex + 1} of {totalQuestions}</p>
      <h2 className="question">{question.question}</h2>

      {question.options.map((opt) => {
        const isSelected = selected === opt
        const isCorrect = opt === question.correct_answer
        const cls = showResult ? (isCorrect ? 'option correct' : (isSelected ? 'option wrong' : 'option')) : 'option'
        return (
          <div key={opt} className={cls} onClick={() => !showResult && setSelected(opt)}>
            {opt}
          </div>
        )
      })}

      <div style={{flex:1}} />

      {!showResult && selected && (
        <button className="primary" onClick={() => setShowResult(true)}>Check Answer</button>
      )}

      {showResult && (
        <button onClick={() => { onAnswer(selected === question.correct_answer); setSelected(null); setShowResult(false); }}>
          {currentIndex === totalQuestions - 1 ? 'Finish' : 'Next'}
        </button>
      )}
    </div>
  )
}

function ResultsScreen({ score, total, onPlayAgain }) {
  return (
    <div className="center">
      <h1>Quiz Complete!</h1>
      <p>You scored</p>
      <h2 className="score">{score} / {total}</h2>
      <button className="secondary" onClick={onPlayAgain}>Play Again</button>
    </div>
  )
}

export default function App() {
  const [state, setState] = useState('initial') // initial, loading, quiz, results, error
  const [quiz, setQuiz] = useState(null)
  const [index, setIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [error, setError] = useState('')

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

  return (
    <div className="app">
      {state === 'initial' && <InitialScreen onStart={start} />}
      {state === 'loading' && <LoadingScreen />}
      {state === 'error' && <ErrorScreen message={error} onRetry={start} />}
      {state === 'quiz' && quiz && (
        <QuizScreen question={quiz[index]} currentIndex={index} totalQuestions={quiz.length} onAnswer={handleAnswer} />
      )}
      {state === 'results' && <ResultsScreen score={score} total={quiz.length} onPlayAgain={playAgain} />}
    </div>
  )
}
