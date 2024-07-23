from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text','cour']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
        }

ChoiceFormSet = forms.inlineformset_factory(
    Question, Choice, fields=('text', 'is_correct'), extra=3,can_delete=False,
    widgets={
        'text': forms.TextInput(attrs={'class': 'form-control'}),
        'is_correct   ': forms.CheckboxInput( ),
    }
)

class ReponseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(ReponseForm, self).__init__(*args, **kwargs)
        for question in questions:
            choices = [(choice.id, choice.text) for choice in question.choices.all()]
            self.fields['question_'+str(question.id)] = forms.ChoiceField(
                label=question.text,
                choices=choices,
                widget=forms.RadioSelect( )
            )

