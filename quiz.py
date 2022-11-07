from tkinter import Tk, Canvas, StringVar, Label, Radiobutton, Button, messagebox
import random
# import requests
# from tkinter import *

THEME_COLOUR = "#1E1210"
# parameters = {
#     "amount" : 10,
#     "difficulty" : "hard",
#     "type" : "boolean"
# }

# response = requests.get(url="https://opentdb.com/api.php?amount=10&category=9&difficulty=hard&type=boolean" , params = parameters)
# question_data = response.json()['results']
    

tips = ['The more questions you answer right, the faster you will travel!','You will have a limited amount of time to complete the maze!']
tip = tips[random.randint(0,len(tips)-1)]


class Question:
    def __init__(self, question, correct_answer,choices):
        self.question_text = question
        self.correct_answer = correct_answer
        self.choices = choices



class QuizBrain:
    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list
    def check_answer(self,user_answer):
        correct_answer = self.current_question.correct_answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False

        
        
    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = self.current_question.question_text
        return "Q." + str(self.question_number) +":" + str(q_text)
    def still_has_questions(self):
        return self.question_number < len(self.question_list)
                

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain) -> None:
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quiz")
        self.window.geometry("850x530")
        self.display_title()

        self.canvas = Canvas(width = 800, height = 250)
        self.question_text = self.canvas.create_text(400, 125, text = "Question here", width = 680, fill = THEME_COLOUR, font = ("Ariel", 15, "italic"))
        self.canvas.grid(row = 2, column = 0, columnspan = 2, pady = 50)
        self.display_question()

        self.user_answer = StringVar()
        self.opts = self.radio_buttons()
        self.display_options()
        self.feedback = Label(self.window, pady = 10, font = ("Ariel", 15, "bold"))
        self.feedback.place(x=300,y=380)
        self.buttons()
        self.window.mainloop()

    def display_title(self):
        title = Label(self.window, text = tip , width = 50, bg = "blue", fg = "white", font = ("ariel",10,"bold"))
        title.place(x=0,y=2)

    def display_question(self):
        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text = q_text)

    def radio_buttons(self):
        choice_list = []
        y_pos = 220

        while len(choice_list) < 4:
            radio_btn = Radiobutton(self.window, text = "", variable = self.user_answer, value = "", font = ("ariel", 14))
            choice_list.append(radio_btn)
            radio_btn.place(x=200, y = y_pos)
            y_pos += 40
        return choice_list
    
    def display_options(self):
        val = 0
        self.user_answer.set(None)  # type: ignore

        for option in self.quiz.current_question.choices:
            self.opts[val]['text'] = option
            self.opts[val]['value'] = option
            val += 1
    
    def next_btn(self):
        if self.quiz.check_answer(self.user_answer.get()):
            self.feedback["fg"] = "green"
            self.feedback["text"] = "Correct!"
        else:
            self.feedback["fg"] = "red"
            self.feedback["text"] = "Not quite!"
        if self.quiz.still_has_questions():
            self.display_question()
            self.display_options()
        else:
            self.window.destroy()
    
    def buttons(self):
        next_button = Button(self.window, text="Next", command=self.next_btn, width=10, bg="blue", fg="white", font=("ariel", 16, "bold"))
        next_button.place(x=350, y=460)
        quit_button = Button(self.window, text="Quit", command=self.window.destroy, width=5, bg="purple", fg="white", font=("ariel", 16, " bold"))
        quit_button.place(x=700,y=50)

# question_bank = []

# for question in question_data:
#     question_text = question["question"]
#     question_answer = question["correct_answer"]
#     new_question = Question(question_text, question_answer)
#     question_bank.append(new_question)
    
# quiz = QuizBrain(question_bank)

# while quiz.still_has_questions():
#     quiz.next_question()
    
# else:
#     print("Quiz completed, you scored: " + str(quiz.score))
    
    








            

