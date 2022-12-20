from django.db import models
from django.contrib.auth.models import User

import json
# ONE QUIZ
# All scores are in percentages

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def average_score(self):
        studentAttempts = QuizAttempt.objects.filter(student = self)
        if studentAttempts == None:
            return 0
        
       
        total = 0
        counter = 0
        for attempt in studentAttempts:
            total += attempt.score
            counter += 1
        
        if total == 0:
            return 0

        average = round(total/counter, 1)

        return average
        


        
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
# GET STUDENT INFORMATION FUNCTION
class QuizContent(models.Model):
    question = models.TextField()
    answers_raw = models.TextField()

    @property
    def percentage_correct(self):
        tally = 0
        total = 0
        for question in QuestionAttempt.objects.filter(quiz_content = self):
            if question.correct:
                tally += 1
            total += 1
        
        if total == 0:
            return 0

        return round(tally/total * 100, 1)
    
    @property
    def answers(self):
        try:

            return json.loads(self.answers_raw)
        except ValueError as e:
            print(e)

    @property
    def correct_answers(self):
        correct_answers = []
        answers = json.loads(self.answers_raw)
        for key in answers.keys():
            if answers[key] == 'correct':
                correct_answers.append(key)
        return correct_answers

    def __str__(self):
        return self.question

class QuizAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete= models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    

    @property
    def score(self): #As a percentage
        tally = 0
        total = 0
        for question in QuestionAttempt.objects.filter(quiz_attempt = self):
            if question.correct:
                tally += 1
            total += 1
        
        if total == 0:
            return 0

        return round(tally/total * 100, 1)

    def __str__(self):
        return "Quiz: " + str(self.student) + " : " + str(self.date_time.date()) + " : " + "%" + str(self.score)

class QuestionAttempt(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    quiz_content = models.ForeignKey(QuizContent, on_delete=models.CASCADE, blank=True, null=True)
    submitted_answer = models.TextField()

    @property
    def correct(self):
        try:
            submitted_answers = json.loads(self.submitted_answer)
        except:
            submitted_answers = []
        correct_answers = self.quiz_content.correct_answers
        for answer in submitted_answers:
            if not answer in correct_answers:
                return False
        
        for answer in correct_answers:
            if not answer in submitted_answers:
                return False
        
        return True
        
    # correct = models.BooleanField(blank=True, null=True) #Blank or Null just means it hasn't been answered

    def __str__(self):
        return 'Question attempt of ' + str(self.quiz_attempt)
        # return str(self.correct)
    