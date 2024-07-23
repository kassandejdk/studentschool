# forms.py
from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'correct_answer','cour']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control'}),
        }
class ReponseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(ReponseForm, self).__init__(*args, **kwargs)
        for question in questions:
            self.fields['question_'+str(question.id)] = forms.CharField(
                label=question.text, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'})
            )
