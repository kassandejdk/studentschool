
from django.db import models
from courses.models import Course

class Question(models.Model):
    cour = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='choices')
    text = models.CharField(max_length=255)

    
    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question,related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

# Create your models here.
