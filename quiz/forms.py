from django import forms
from django.contrib.auth.forms import UserCreationForm
# from .models import Question, Answer
# from .models import (User, QuizType, Quiz, Taker, Question,
#                      Answer, TakenQuiz, TakerAnswer)
from .models import User, Question, Answer, Quiz

#
# class CreatorSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_creator = True
#         user.save()
#         return user
#
#
# class TakerSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_taker = True
#         user.save()
#         return user
#
#
# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['question']
#
#
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']
#
#
# class TakeQuizForm(forms.ModelForm):
#     answer = forms.ModelChoiceField(
#         queryset=Answer.objects.none(),
#         widget=forms.RadioSelect(),
#         required=True,
#     )
#
#     class Meta:
#         model = TakerAnswer
#         fields = ['answer']
#
#     def __init__(self, *args, **kwargs):
#         question = kwargs.pop('question')
#         super().__init__(*args, **kwargs)
#         self.fields['answer'].queryset = question.answers.order_by('question')


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

#
# class QuestionModelForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = '__all__'
#
#         # widgets = {
#         #     'field': forms.HiddenInput()
#         # }
#
#
# class AnswerModelForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = ['answer_text']
#
#         # widgets = {
#         #     'field': forms.HiddenInput()
#         # }
#
