# -*- coding: utf-8 -*-
from courses.forms import AddCourseForm
from courses.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from itertools import chain
from django.http import Http404
from registration.forms import RegistrationForm as AddUser
from source.forms import UpdateForm

def home(request):
    context = {
        "title": "eLearning",
    }

    return render(request, "home.html", context)


def about(request):
    context = {
        "title": "About",
    }

    return render(request, "users/about.html", context)


def contact(request):
    contact_form = Contact(request.GET or None)

    context = {
        "title": "Contact",
        "contact_form": contact_form,
    }

    if contact_form.is_valid():
        sender = contact_form.cleaned_data.get("sender")
        subject = contact_form.cleaned_data.get("subject")
        from_email = contact_form.cleaned_data.get("email")
        message = contact_form.cleaned_data.get("message")
        message = 'Sender:  ' + sender + '\nFrom:  ' + from_email + '\n\n' + message
        send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=True)
        success_message = "We appreciate you contacting us, one of our Customer Service colleagues will get back" \
                          " to you within a 24 hours."
        messages.success(request, success_message)

        return redirect(reverse('contact'))

    return render(request, "users/contact.html", context)


@login_required
def profile(request):
    if request.user.is_site_admin:
        return redirect(reverse('admin'))

    elif request.user.is_professor:
        return redirect(reverse('professor'))

    return redirect(reverse('student'))


@user_passes_test(lambda user: user.is_site_admin)
def admin(request):
    add_user_form = AddUser(request.POST or None)
    queryset = UserProfile.objects.all()
        
    search = request.GET.get("search")
    if search:
        queryset = queryset.filter(username__icontains=search)
    for instance in queryset:
        print('instance : ',instance,'\n')

    context = {
        "title": "Admin",
        "add_user_form": add_user_form,
        "queryset": queryset,

    }
    if add_user_form.is_valid():
        instance = add_user_form.save(commit=False)
        passwd = add_user_form.cleaned_data.get("password")
        instance.password = make_password(password=passwd,
                                          salt='salt', )
        instance.save()
        reverse('profile')

    return render(request, "users/sysadmin_dashboard.html", context)



@user_passes_test(lambda user: user.is_professor)
def professor(request):
    add_course_form = AddCourseForm(request.POST or None)
    queryset_course = Course.objects.filter(user_id=request.user.id)

    queryset_cours = Course.objects.filter(Q(user__username=request.user) and Q(id=request.user.id)).prefetch_related('questions')
    queryset_courses = Course.objects.filter(Q(user__username=request.user) and Q(id=request.user.id)).prefetch_related('choices')



    context = {
        "title": "Professor",
        "add_course_form": add_course_form,
        "queryset_cours": queryset_cours,
        "queryset_course": queryset_course,
        "queryset_courses": queryset_courses,


    }

    if add_course_form.is_valid():
        course_name = add_course_form.cleaned_data.get("course_name")
        instance = add_course_form.save(commit=False)
        instance.niveau = request.POST.get("niveau")
        instance.user = request.user
        instance.save()
        return redirect(reverse('professor_course', kwargs={'course_name': course_name}))

    return render(request, "users/professor_dashboard.html", context)


@login_required
def student(request):
    queryset = Course.objects.filter(pk=request.user.pk)
    user_data = get_object_or_404(UserProfile,pk=request.user.pk)
    if request.method == 'POST':
        form = UpdateForm(request.POST,instance=user_data)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    else:
        user_data.password = ""
        form = UpdateForm(instance=user_data)

    context = {
        "queryset": queryset,
        "title": request.user.first_name,
        "form":form,
    }
    return render(request, "users/student_dashboard.html", context)


@user_passes_test(lambda user: user.is_site_admin)
def update_user(request, username):
    user = UserProfile.objects.get(username=username)
    data_dict = {'username': user.username, 'email': user.email}
    update_user_form = UpdateForm(initial=data_dict, instance=user)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        "title": "Edit",
        "update_user_form": update_user_form,
        "path": path,
        "redirect_path": redirect_path,
    }

    if request.POST:
        user_form = UpdateForm(request.POST, instance=user)

        if user_form.is_valid():
            instance = user_form.save(commit=False)
            passwd = user_form.cleaned_data.get("password")

            if passwd:
                instance.password = make_password(password=passwd,
                                                  salt='salt', )
            instance.save()

            return redirect(reverse('profile'))

    return render(request, "users/edit_user.html", context)


@user_passes_test(lambda user: user.is_site_admin)
def delete_user(request, username):
    user = UserProfile.objects.get(username=username)
    user.delete()
    return redirect(reverse('profile'))


@login_required
def course_homepage(request, course_name):
    chapter_list = Chapter.objects.filter(course__course_name=course_name)

    if chapter_list:
        return redirect(reverse(student_course, kwargs={'course_name': course_name,
                                                        "slug": chapter_list[0].slug}))
    else:
        warning_message = "Actuellement, il n'y a pas de chapitres pour ce cours "
        messages.warning(request, warning_message)
        return redirect(reverse('courses'))


@login_required
def student_course(request, course_name, slug=None):
    course = Course.objects.get(course_name=course_name)
    chapter_list = Chapter.objects.filter(course=course)
    chapter = Chapter.objects.get(course__course_name=course_name, slug=slug)
    text = TextBlock.objects.filter(text_block_fk=chapter)
    videos = Video.objects.filter(yt_link_fk=chapter.id)
    files = FileUpload.objects.filter(file_fk=chapter)
    user = request.user
    course.view+=1
    vue = course.view
    course.save()

    if user in course.students.all() or user.is_professor or user.is_site_admin or course.for_everybody:
        result_list = sorted(
            chain(text, videos, files),
            key=lambda instance: instance.date_created)
            

        context = {
            "course_name": course_name,
            "chapter_list": chapter_list,
            "chapter_name": chapter.chapter_name,
            "slug": chapter.slug,
            "result_list": result_list,
            "title": course_name + ' : ' + chapter.chapter_name,
            "course_id":course.id,
        }

        return render(request, "users/student_courses.html", context)

    else:
        raise Http404
