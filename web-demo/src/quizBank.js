const q = (question, options, correct_answer, extra = {}) => ({
  question,
  options,
  correct_answer,
  ...extra,
})

const textQuestions = [
  q('How do you say "good morning"?', ['Ohayou', 'Konnichiwa', 'Konbanwa', 'Sayonara'], 'Ohayou'),
  q('How do you say "good evening"?', ['Konbanwa', 'Ohayou', 'Arigatou', 'Mata ne'], 'Konbanwa'),
  q('Which phrase means "thank you very much"?', ['Domo arigatou gozaimasu', 'Onegaishimasu', 'Sumimasen', 'Oyasumi'], 'Domo arigatou gozaimasu'),
  q('Translate "I go to school".', ['Gakkou ni ikimasu', 'Gakkou ni imasu', 'Gakkou de tabemasu', 'Gakkou kara kaerimasu'], 'Gakkou ni ikimasu'),
  q('Which particle fits: Watashi wa Taro ___ desu.', ['wa', 'ga', 'o', 'ni'], 'wa'),
  q('What is the polite request phrase for "please"?', ['Onegaishimasu', 'Arigatou', 'Hai', 'Itadakimasu'], 'Onegaishimasu'),
  q('Choose the verb that means "to eat".', ['tabemasu', 'nomimasu', 'ikimasu', 'mimasu'], 'tabemasu'),
  q('Which word means "water"?', ['mizu', 'sora', 'yama', 'ki'], 'mizu'),
  q('Select the polite way to say "sorry".', ['Sumimasen', 'Hai', 'Iie', 'Dewa mata'], 'Sumimasen'),
  q('Translate "I understand".', ['Wakarimasu', 'Shirimasu', 'Mimasu', 'Kimasu'], 'Wakarimasu'),
  q('Which word means "today"?', ['kyou', 'ashita', 'kinou', 'sugu'], 'kyou'),
  q('Which word means "friend"?', ['tomodachi', 'sensei', 'gakusei', 'kazoku'], 'tomodachi'),
  q('Translate "See you tomorrow".', ['Mata ashita', 'Mata kyou', 'Oyasumi', 'Itadakimasu'], 'Mata ashita'),
  q('Which phrase means "I think"?', ['to omoimasu', 'to tabemasu', 'to ikimasu', 'to nomimasu'], 'to omoimasu'),
  q('Which expression is used before eating?', ['Itadakimasu', 'Gochisousama', 'Otsukaresama', 'Yokatta'], 'Itadakimasu'),
]

const audioQuestions = [
  q('You hear: "Ohayou gozaimasu." What does it mean?', ['Good morning', 'Good night', 'Thank you', 'Excuse me'], 'Good morning', { audioCue: 'Ohayou gozaimasu.' }),
  q('You hear: "Onegaishimasu." What is the best meaning?', ['Please', 'Goodbye', 'Yes', 'No'], 'Please', { audioCue: 'Onegaishimasu.' }),
  q('You hear: "Arigatou gozaimasu." What is being said?', ['Thank you very much', 'See you later', 'I do not know', 'Good afternoon'], 'Thank you very much', { audioCue: 'Arigatou gozaimasu.' }),
  q('You hear: "Sumimasen." What does the speaker mean?', ['Sorry / excuse me', 'Please sit down', 'I am hungry', 'Let us go'], 'Sorry / excuse me', { audioCue: 'Sumimasen.' }),
  q('You hear: "Mizu o kudasai." What should you bring?', ['Water', 'Rice', 'Tea', 'Bread'], 'Water', { audioCue: 'Mizu o kudasai.' }),
  q('You hear: "Gakkou ni ikimasu." What is the meaning?', ['I go to school', 'I sleep at school', 'I eat at school', 'I return from school'], 'I go to school', { audioCue: 'Gakkou ni ikimasu.' }),
  q('You hear: "Watashi wa gakusei desu." What does it mean?', ['I am a student', 'I am a teacher', 'I am a friend', 'I am busy'], 'I am a student', { audioCue: 'Watashi wa gakusei desu.' }),
  q('You hear: "Kyou wa samui desu." What is the speaker saying about today?', ['It is cold', 'It is hot', 'It is raining', 'It is sunny'], 'It is cold', { audioCue: 'Kyou wa samui desu.' }),
  q('You hear: "Mata ashita." What does it mean?', ['See you tomorrow', 'See you tonight', 'Hello again', 'Good job'], 'See you tomorrow', { audioCue: 'Mata ashita.' }),
  q('You hear: "Oyasumi nasai." What is the meaning?', ['Good night', 'Good morning', 'Welcome', 'Good luck'], 'Good night', { audioCue: 'Oyasumi nasai.' }),
  q('You hear: "Tomodachi to aimasu." What is the action?', ['Meet a friend', 'Cook dinner', 'Read a book', 'Buy clothes'], 'Meet a friend', { audioCue: 'Tomodachi to aimasu.' }),
  q('You hear: "Kore wa nan desu ka." What is being asked?', ['What is this?', 'How are you?', 'Where are you?', 'How much is it?'], 'What is this?', { audioCue: 'Kore wa nan desu ka.' }),
  q('You hear: "Hai, wakarimashita." What does it mean?', ['Yes, I understood', 'No, I cannot', 'Please wait', 'Thank you'], 'Yes, I understood', { audioCue: 'Hai, wakarimashita.' }),
  q('You hear: "Doushite?" What is the meaning?', ['Why?', 'When?', 'Who?', 'Where?'], 'Why?', { audioCue: 'Doushite?' }),
  q('You hear: "Ki o tsukete." What is the best meaning?', ['Take care', 'Sit down', 'Open the door', 'Write it'], 'Take care', { audioCue: 'Ki o tsukete.' }),
]

const writingQuestions = [
  q('Which written form is correct for "good morning"?', ['ohayou', 'ohayoou', 'ohayoo', 'ohayu'], 'ohayou'),
  q('Which written form is correct for "thank you very much"?', ['domo arigatou gozaimasu', 'domo arigato gozaimasu', 'domo arigatou gozaimashu', 'damo arigatou gozaimasu'], 'domo arigatou gozaimasu'),
  q('Which written form is correct for "school"?', ['gakkou', 'gakko', 'gakkoo', 'gakkow'], 'gakkou'),
  q('Which written form is correct for "friend"?', ['tomodachi', 'tomodaci', 'tomodachih', 'tomodace'], 'tomodachi'),
  q('Which written form is correct for "water"?', ['mizu', 'misu', 'mizou', 'mizuo'], 'mizu'),
  q('Which written form is correct for "yesterday"?', ['kinou', 'kino', 'kouni', 'kinyou'], 'kinou'),
  q('Which written form is correct for "today"?', ['kyou', 'kyo', 'kyoo', 'kyouu'], 'kyou'),
  q('Which written form is correct for "tomorrow"?', ['ashita', 'ashitaa', 'asita', 'ashiti'], 'ashita'),
  q('Which written form is correct for "please"?', ['onegaishimasu', 'onegai shimasu', 'onegai shimassu', 'onegai shimas'], 'onegaishimasu'),
  q('Which written form is correct for "sorry / excuse me"?', ['sumimasen', 'sumimasane', 'sumimassen', 'sumimase'], 'sumimasen'),
  q('Which written form is correct for "I understand"?', ['wakarimasu', 'wakarimashu', 'wakarimasun', 'wakarimasu'], 'wakarimasu'),
  q('Which written form is correct for "I eat"?', ['tabemasu', 'tabemassu', 'tabemashu', 'tabemasu'], 'tabemasu'),
  q('Which written form is correct for "I go"?', ['ikimasu', 'ikimashu', 'ikimasun', 'ikimas'], 'ikimasu'),
  q('Which written form is correct for "I drink"?', ['nomimasu', 'nomimassu', 'nomimashu', 'nomimas'], 'nomimasu'),
  q('Which written form is correct for "see you tomorrow"?', ['mata ashita', 'mata ashitaa', 'mata asita', 'mata ashitaa'], 'mata ashita'),
]

const listeningQuestions = [
  q('The speaker says: "Watashi wa Taro desu." What is the best response?', ['Nice to meet you, Taro.', 'I am tired today.', 'Please open the door.', 'It is raining now.'], 'Nice to meet you, Taro.', { audioCue: 'Watashi wa Taro desu.' }),
  q('The speaker says: "Gakkou ni ikimasu." What is the meaning?', ['I go to school.', 'I came from school.', 'I stay at school.', 'I study at home.'], 'I go to school.', { audioCue: 'Gakkou ni ikimasu.' }),
  q('The speaker says: "Mizu o kudasai." What should you do?', ['Give water.', 'Read a book.', 'Close the window.', 'Leave now.'], 'Give water.', { audioCue: 'Mizu o kudasai.' }),
  q('The speaker says: "Kyou wa samui desu." What is the speaker describing?', ['Today is cold.', 'Today is late.', 'Today is long.', 'Today is busy.'], 'Today is cold.', { audioCue: 'Kyou wa samui desu.' }),
  q('The speaker says: "Mata ashita." What does the person mean?', ['See you tomorrow.', 'See you yesterday.', 'Good evening.', 'Please wait.'], 'See you tomorrow.', { audioCue: 'Mata ashita.' }),
  q('The speaker says: "Domo arigatou gozaimasu." What is the meaning?', ['Thank you very much.', 'Excuse me.', 'Good morning.', 'I am sorry.'], 'Thank you very much.', { audioCue: 'Domo arigatou gozaimasu.' }),
  q('The speaker says: "Onegaishimasu." Which response fits best?', ['Please / kindly do it.', 'No problem.', 'I am asleep.', 'Goodbye.'], 'Please / kindly do it.', { audioCue: 'Onegaishimasu.' }),
  q('The speaker says: "Sumimasen." What is the likely meaning?', ['Sorry / excuse me.', 'Please come in.', 'I am happy.', 'See you soon.'], 'Sorry / excuse me.', { audioCue: 'Sumimasen.' }),
  q('The speaker says: "Ashita, tomodachi to aimasu." What will happen?', ['Meet a friend tomorrow.', 'Cook dinner tonight.', 'Buy a train ticket.', 'Go to sleep early.'], 'Meet a friend tomorrow.', { audioCue: 'Ashita, tomodachi to aimasu.' }),
  q('The speaker says: "Kore wa nan desu ka." What is the speaker asking?', ['What is this?', 'Who is that?', 'How much is it?', 'Where are you?'], 'What is this?', { audioCue: 'Kore wa nan desu ka.' }),
  q('The speaker says: "Oyasumi nasai." What should you understand?', ['Good night.', 'Good afternoon.', 'Thank you.', 'Welcome.'], 'Good night.', { audioCue: 'Oyasumi nasai.' }),
  q('The speaker says: "Hai, wakarimashita." What does it mean?', ['Yes, I understood.', 'No, I cannot.', 'I am leaving.', 'Please repeat.'], 'Yes, I understood.', { audioCue: 'Hai, wakarimashita.' }),
  q('The speaker says: "Doushite?" What is the meaning?', ['Why?', 'When?', 'Who?', 'How many?'], 'Why?', { audioCue: 'Doushite?' }),
  q('The speaker says: "Ki o tsukete." What is the speaker wishing?', ['Take care.', 'Sit down.', 'Stand up.', 'Move faster.'], 'Take care.', { audioCue: 'Ki o tsukete.' }),
  q('The speaker says: "Yoroshiku onegaishimasu." What is the best interpretation?', ['Please treat me well.', 'See you tomorrow.', 'Good afternoon.', 'I am hungry.'], 'Please treat me well.', { audioCue: 'Yoroshiku onegaishimasu.' }),
]

const makePlayground = (id, title, description, hint, questions) => ({
  id,
  title,
  description,
  hint,
  questions,
})

export const quizPlaygrounds = [
  makePlayground('text', 'Text Playground', 'Read short Japanese prompts and pick the best translation.', 'Reading and translation drills', textQuestions),
  makePlayground('audio', 'Audio Playground', 'Listen to the cue and choose the meaning you heard.', 'Audio cue recognition', audioQuestions),
  makePlayground('writing', 'Writing Playground', 'Choose the correct written form and spelling.', 'Spelling and written form', writingQuestions),
  makePlayground('listening', 'Listening Playground', 'Hear a line and respond with the best interpretation.', 'Comprehension and response', listeningQuestions),
]

const normalize = (value) => String(value || '').trim().toLowerCase().replace(/\s+/g, ' ')

const fallbackValidation = (playground, question, selectedAnswer) => ({
  section: playground.title,
  question: question.question,
  selected_answer: selectedAnswer,
  correct_answer: question.correct_answer,
  gemma_answer: question.correct_answer,
  gemma_response: 'Gemma service unavailable, so the local answer key was used.',
  is_correct: normalize(selectedAnswer) === normalize(question.correct_answer),
  gemma_agrees: true,
  confidence_score: 0.8,
  validation_notes: 'Local fallback validation used because the model endpoint was unavailable.',
  response_time_ms: 0,
  model_name: 'gemma-e2b',
  provider: 'local-fallback',
})

export async function validateChoiceWithGemma({ playground, question, selectedAnswer }) {
  try {
    const response = await fetch('/api/results/validate_choice/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        section: playground.title,
        question: question.question,
        options: question.options,
        selected_answer: selectedAnswer,
        correct_answer: question.correct_answer,
        explanation: question.explanation || '',
      }),
    })

    if (!response.ok) {
      throw new Error(`Validation request failed with status ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    return fallbackValidation(playground, question, selectedAnswer)
  }
}
