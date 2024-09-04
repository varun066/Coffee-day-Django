from django import forms
from django.shortcuts import render,redirect
from .models import Item,Menu, QA

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields = ['name', 'item_type', 'custom_id', 'price', 'description','image']


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'items']
        widgets = {
            'items': forms.CheckboxSelectMultiple,  # Allows selecting multiple items using checkboxes
        }


class SuperuserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = QA
        fields = ['question']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = QA
        fields = ['answer']