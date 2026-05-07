export async function generateQuiz() {
  // Simulate network / computation delay
  await new Promise((res) => setTimeout(res, 1200))

  return {
    quiz: [
      {
        question: "Translate: 'good morning'",
        options: ["Ohayō", "Konnichiwa", "Konbanwa", "Sayonara"],
        correct_answer: "Ohayō"
      },
      {
        question: "Translate: 'I will go to school'",
        options: ["Gakkō ni ikimasu", "Gakkō ni imasu", "Gakkō ni kaerimasu", "Gakkō ni tabemasu"],
        correct_answer: "Gakkō ni ikimasu"
      },
      {
        question: "Choose the polite particle: 'please'",
        options: ["Onegaishimasu", "Arigatō", "Sumimasen", "Hai"],
        correct_answer: "Onegaishimasu"
      }
    ]
  }
}
