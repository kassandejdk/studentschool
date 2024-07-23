from django.db import models
from courses.models import Course

class Question(models.Model): 
    cour = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='questions')
    text = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255,default="")
   

    def __str__(self):
        return self.text

        

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name = 'choices',on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

# Create your models here.
