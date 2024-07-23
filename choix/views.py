from django.shortcuts import render, redirect,get_object_or_404
from .forms import QuestionForm, ChoiceFormSet,ReponseForm
from .models import Question, Choice
from courses.models import Course,Chapter
from django.contrib.auth.decorators import login_required,user_passes_test


def is_professor_or_admin(user):
    return user.is_authenticated and (user.is_professor or user.is_site_admin)


@login_required
@user_passes_test(lambda user:is_professor_or_admin)
def ajouter_choix(request,course_id):
    course = Course.objects.get(id=course_id) 
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.cour = course
            question.save()
            choices = formset.save(commit=False)
            for choice in choices:
                choice.question = question
                choice.save()
            return redirect('ajouter_choix',course_id=course_id)
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()
    context = {
        'form':form,
        'formset':formset,
        'course':course,
    }
    return render(request, 'qcm/ajouter_choix.html',context)


@login_required
def verifier_choix(request,course_id,slug):
    print(course_id)
    
    course = Course.objects.get(id=course_id)
    questions = Question.objects.filter(cour_id = course_id)
    if request.method == 'POST':
        form = ReponseForm(request.POST, questions=questions)
        if form.is_valid():
            correct_answers = []
            score = 0
            total_choix = questions.count()
            bonnes_choix = []

            for question in questions:
                selected_choice_id = form.cleaned_data['question_'+str(question.id)]
                selected_choice = get_object_or_404(Choice, id=selected_choice_id)
                is_correct = selected_choice.is_correct
                if is_correct:
                    score += 1

                correct_answers.append((question.text, selected_choice.text, is_correct))

                correct_choice = question.choices.filter(is_correct=True).first()
                print(correct_choice)
                #print("===================",question.choices)
                print(question.text,"=====choic=========",correct_choice.text)
                bonnes_choix.append((question.text, correct_choice.text))
            if course.note_question < score:
                course.note_question = score
                course.save()
            grade = (score / total_choix) * 20 
            
            context = {
                'slug':slug,
                'course_name':course.course_name,
                'correct_answers': correct_answers,
                'grade': grade,
                'score': score,
                'total_choix': total_choix,
                'bonnes_choix': bonnes_choix,
                'course_id':course_id,
            }
            
            return render(request, 'qcm/afficher_choix.html', context)
    else:
        form = ReponseForm(questions=questions)
    context = {
            'slug':slug,
            'course_name':course.course_name,
            'form':form,
        }
    return render(request, 'qcm/reponse_choix.html', context)

@login_required
def liste_choix(request):
    if request.user.is_professor  or request.user.is_site_admin:
        questions = Question.objects.all()
    else:
        courses = Course.objects.filter(niveau=request.user.niveau)
        questions = Question.objects.filter(cour__in=courses)
    return render(request, 'qcm/liste_choix.html', {'questions': questions})



@login_required
@user_passes_test(is_professor_or_admin)
def editer_choix(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = ChoiceFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('liste_choix')
    else:
        form = QuestionForm(instance=question)
        formset = ChoiceFormSet(instance=question) 
    return render(request, 'qcm/editer_choix.html', {'form': form, 'formset': formset})

    
@login_required
@user_passes_test(is_professor_or_admin) 
def supprimer_choix(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('liste_choix')
    return render(request, 'qcm/supprimer_choix.html', {'question': question})





@login_required
def suivre(request,pk):
    print(pk)
    chapter = Chapter.objects.get(pk=pk)
    course = Course.objects.get(pk=pk)
    question = Question.objects.filter(cour_id=course).count()
    if course.note_question > 5:
        grade = (course.note_question / question) * 20 
        context ={
            'course_name':course.course_name,
            'slug':chapter.slug,
            'grade':grade,
        }
        return render(request,'qcm/suivre.html',context)
    elif (course.note_question> 5 and course.note_question<15):
        grade = (course.note_question / question) * 20 
        context ={
            'course_name':course.course_name,
            'slug':chapter.slug,
            'grade':grade,
        }
        return render(request,'qcm/suivre.html',context)
    elif (course.note_question> 15 and course.note_question<20):
        grade = (course.note_question / question) * 20 
        context ={
            'course_name':course.course_name,
            'slug':chapter.slug,
            'grade':grade,
        }
        return render(request,'qcm/suivre.html',context)
    elif course.note_question==20:
        grade = (course.note_question / question) * 20 
        return render (request,'qcm/suivre.html',{'grade':grade,})
    else:
        grade = (course.note_question / question) * 20 
        context ={
            'course_name':course.course_name,
            'slug':chapter.slug,
            'grade':grade,
        }
        return render(request,'qcm/suivre.html',context)
# Create your views here.