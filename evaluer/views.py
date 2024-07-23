from django.shortcuts import render, redirect,get_object_or_404
from .models import Question, Answer
from .forms import ReponseForm,QuestionForm
from courses.models import Course,Chapter
from django.contrib.auth.decorators import user_passes_test,login_required


def is_professor_or_admin(user):
    return user.is_authenticated and (user.is_professor or user.is_site_admin)

@login_required 
@user_passes_test(lambda user: is_professor_or_admin)
def ajouter_question(request,course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        print("Pas de chapitre")
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.course = course
            question.save()

            return redirect('ajouter_question',course_id=course_id) 
    else:
        form = QuestionForm()
    context = {
        'form':form,
        'course':course,
    }
    return render(request, 'evaluer/ajouter_questions.html', context)



@login_required
def verifier_reponse(request,course_id,slug):
    try:
        chapter = Chapter.objects.get(id=course_id)
        print("chapitre OKLM")
    except Chapter.DoesNotExist:
        print("Pas de chapitre")
    course=Course.objects.get(id=course_id)
    questions = Question.objects.filter(cour_id = course_id)
    bonnes_reponses = [(question.text, question.correct_answer) for question in questions]
    if request.method == 'POST':
        form = ReponseForm(request.POST, questions=questions)
        if form.is_valid():
            correct_answers = []
            score = 0
            total_questions = questions.count()

            for question in questions:
                user_answer = form.cleaned_data['question_'+str(question.id)]
                is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()

                if is_correct:
                    score += 1

                correct_answers.append((question.text, user_answer, is_correct))
            if course.note_question < score:
                course.note_question = score
                course.save()

            grade = (score / total_questions) * 20 

            context = {
                'slug':slug,
                'course_name':course.course_name,
                'correct_answers': correct_answers,
                'grade': grade,
                'score': score,
                'total_questions': total_questions,
                'bonnes_reponses': bonnes_reponses,
                'course_id':course_id,
            }
            return render(request, 'evaluer/afficher_bonnes_reponses.html', context)
    else:
        form = ReponseForm(questions=questions)
        context = {
            'slug':slug,
            'course_name':course.course_name,
            'form':form,
        }
    return render(request, 'evaluer/reponse_questions.html', context)

@login_required
def liste_questions(request):
    questions = Question.objects.all()
    return render(request, 'evaluer/liste_questions.html', {'questions': questions})

@login_required
@user_passes_test(lambda user: is_professor_or_admin)
def editer_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('liste_questions')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'evaluer/editer_question.html', {'form': form})

@login_required
@user_passes_test(lambda user: is_professor_or_admin)
def supprimer_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('liste_questions')
    return render(request, 'evaluer/supprimer_question.html', {'question': question})


@login_required
def suivre(request,pk):
    chapter = Chapter.objects.get(pk=pk)
    course = Course.objects.get(pk=pk)
    question = Question.objects.filter(cour_id=course).count()
    if course.note_question> 5:
        grade = (course.note_question/ question) * 20 
        
        return render(request,'suivre.html',{'grade':grade,})
    elif (course.note_choix> 5 and course.note_choix<15):
        grade = (course.note_question/ question) * 20 
        return render(request,'suivre.html',{'grade':grade,})
    elif (course.note_choix> 15 and course.note_choix<20):
        grade = (course.note_question/ question) * 20 
        return render(request,'suivre.html',{'grade':grade,})
    elif course.note_choix==20:
        grade = (course.note_question/ question) * 20 
        return render (request,'suivre.html',{'grade':grade,})
    else:
        grade = (course.note_question/ question) * 20 
        return render(request,'suivre.html',{'grade':grade,})
