"""
URL configuration for QCM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from choix import views


urlpatterns = [
    url(r'^ajouter_choix/(?P<course_id>\d+)/$', views.ajouter_choix, name='ajouter_choix'),
    url(r'^verifier_choix/(?P<course_id>[\w ]+)/(?P<slug>[\w-]+)/$', views.verifier_choix, name='verifier_choix'),
    url(r'^liste_choix/$', views.liste_choix, name='liste_choix'),
    url(r'^editer_choix/(?P<pk>\d+)/$', views.editer_choix, name='editer_choix'),
    url(r'^supprimer_choix/(?P<pk>\d+)/$', views.supprimer_choix, name='supprimer_choix'),
    url(r'^suivre/(?P<pk>\d+)/$',views.suivre, name='suivre'),

]

