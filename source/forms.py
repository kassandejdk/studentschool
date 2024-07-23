# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from users.models import UserProfile
from django.contrib.auth.hashers import  make_password
from django.views.generic import FormView

from django.core.exceptions import ValidationError
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from users.models import UserProfile
from django.http import Http404,HttpResponse

class ConfirmForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email','confirmation_code']

class ConfirmFormBase(TemplateView):

    template_name='registration/registration_complete.html'
    form_class = ConfirmForm

    def get_context_data(self, **kwargs):
        context = super(ConfirmFormBase,self).get_context_data(**kwargs)
        context['form'] = ConfirmForm()  # Ajoutez une instance du formulaire au contexte
        return context

    def post(self, request, *args, **kwargs):
        form = ConfirmForm(request.POST)
        message = ""
        erreur = False
        if form.is_valid():
            email = form.cleaned_data['email']
            confirmation_code = form.cleaned_data['confirmation_code']
            context = {'form': form,'email':'','confirmation_code':''}
            try:
                user = UserProfile.objects.get(email=email)
                if user.confirmation_code == confirmation_code:
                    user.is_active = 1
                    user.save()
                    return redirect('auth_login')
                else:
                    erreur = True
                    message = "Code Incorrect !"
                    context = {'form': form,'message':message,'erreur':erreur}
                    return render(request, self.template_name, context)
            except UserProfile.DoesNotExist:
                    erreur = True
                    message = "Email invalide !"
                    context = {'form': form,'message':message,'erreur':erreur}
                    return render(request, self.template_name, context)
        else:
            context = {'form': form}
            return render(request, self.template_name, context)

class UpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','password','email','numero']
        widgets = {
        'password':forms.PasswordInput(),
        }
    def save(self,commit=True):
        user = super(UpdateForm,self).save(commit=False)
        user.password = make_password(self.cleaned_data['password'])

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if not numero.isdigit():
            
            raise ValidationError("Le numéro doit contenir uniquement des chiifres")
        if len(numero)!=8:
            raise ValidationError("Le numero doi contenir exactement 8 Chiffres.")
        return numero
        if commit:
            user.save()
        return user   



 