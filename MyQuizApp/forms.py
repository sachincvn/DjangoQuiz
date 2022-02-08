from pyexpat import model
from django import forms
from django.db.models import fields
from .models import quizquestion, quiztopics, useranswers, users
from django.core import validators

class AddQuiz(forms.ModelForm):
    class Meta:
        model = quiztopics
        fields = ['quiz_cat','quiz_title','quiz_desc','quiz_url','quiz_thumb']


class AddQuestion(forms.ModelForm):
    class Meta:
        model = quizquestion
        fields = ['qn_cat','qn_title','qn_name','qn_opt1','qn_opt2','qn_opt3','qn_opt4','qn_ans']


class UserAnswer(forms.ModelForm):
    class Meta:
        model = useranswers
        fields = [
            'full_name',
            'username',
            'email_id',
            'qn_cat',
            'qn_name',
            'qn_ans',
        ]
