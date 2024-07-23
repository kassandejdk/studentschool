"""
URL configuration for Evaluation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, url
    2. Add a URL to urlpatterns:  url('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
import views

urlpatterns = [
    #url(r'^courses/', include('courses.urls')),
    url(r'^questions/', views.liste_questions, name='liste_questions'),
    # url(r'^questions/editer/<int:id>/', views.editer_question, name='editer_question'),
    # url(r'^supprimer/<int:id>/', views.supprimer_question, name='supprimer_question'),
    url(r'^ajouter_question/(?P<course_id>\d+)/$', views.ajouter_question, name='ajouter_question'),
    url(r'^verifier_reponse/(?P<course_id>[\w ]+)/(?P<slug>[\w-]+)/$', views.verifier_reponse, name='verifier_reponse'),
    url(r'^editer(?P<pk>\d+)/$',views.editer_question, name='editer_question'),
    url(r'^supprimer(?P<pk>\d+)/$',views.supprimer_question, name='supprimer_question'),
    url(r'^suivre/(?P<pk>\d+)/$',views.suivre, name='suivre'),

]
