import requests
from tkinter import *


parameters = {
    "amount" : 10,
    "difficulty" : "hard",
    "type" : "boolean"
}

response = requests.get(url="https://opentdb.com/api.php?amount=10&category=9&difficulty=hard&type=boolean" , params = parameters)
question_data = response.json()['results']
    





class Question:
    def __init__(self, question, correct_answer):
        self.question_text = question
        self.correct_answer = correct_answer



class QuizBrain:
    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list
    def check_answer(self,user_answer,correct_answer):
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
        
        
    def next_question(self):
        current_question = self.question_list[self.question_number]
        self.question_number += 1
        user_answer = input("Q." + str(self.question_number) + ":" + str(current_question.question_text) + "(True/False):")
        self.check_answer(user_answer, current_question.correct_answer)                                             

    def still_has_questions(self):
        return self.question_number < len(self.question_list)
                


question_bank = []

for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)
    
quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    quiz.next_question()
    
else:
    print("Quiz completed, you scored: " + str(quiz.score))
    
    








            


