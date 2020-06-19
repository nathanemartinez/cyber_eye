from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, resolve
from django.views.generic import (CreateView, DetailView, DeleteView,
                                  UpdateView, ListView, FormView,
                                  TemplateView)
from django.views.generic.edit import FormMixin
from django.contrib.sites.shortcuts import get_current_site

from .forms import QuizForm, AnswerForm
from .models import Quiz, Question


class TakeQuiz(FormView, ListView):
    model = Quiz
    form_class = AnswerForm
    template_name = 'quiz/take_the_test2.html'
    context_object_name = 'questions'
    paginate_by = 1
    # success_url = 'http://127.0.0.1:8000/test/1/?page=2'

    def get_success_url(self):
        # Gets the dictionary
        current_dict = self.get_current_page_number()
        current_page = current_dict[0]
        next_page = current_dict[1]
        has_next = current_dict[2]
        if (next_page is None) or (has_next is not True):
            return reverse('home:home')
        else:
            # /test/1/
            quiz_page = self.request.path
            # /test/1/?page=?
            url = quiz_page + f'?page={next_page}'
            # Domain name
            home_page = self.request.META['HTTP_HOST']
            # Final URL
            final_url = 'http://' + home_page + url
            return final_url

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        quiz = get_object_or_404(Quiz, pk=pk)
        queryset = quiz.question_set.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        quiz = get_object_or_404(Quiz, pk=pk)
        form = self.get_form()
        if form.is_valid():
            form = form.save(commit=False)
            # Get current page number
            qs = self.get_queryset()
            current = self.get_current_page_number()[0]
            pkkk = qs[current - 1].pk
            question = get_object_or_404(Question, pk=pkkk)
            # Save
            form.question = question
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_current_page_number(self):
        # Get the queryset
        queryset = self.get_queryset()
        # Create the paginator
        paginator = self.get_paginator(queryset, 1)
        # Gets the page
        page = self.request.GET.get('page')
        # The page number
        page_number = paginator.get_page(page).number
        # Is there a next page?
        has_next = paginator.page(page_number).has_next()
        if has_next:
            next_page = paginator.get_page(page_number).next_page_number()
            return page_number, next_page, has_next
        else:
            return page_number, None, has_next


# from .models import QuizTaker, Test, Question, Answer
# from .forms import QuestionModelForm, AnswerModelForm
#
# class TestListView(LoginRequiredMixin, ListView):
#     model = Test
#     template_name = 'quiz/quiz/test_list.html'
#     context_object_name = 'tests'
#
#     def get_queryset(self):
#         return Test.objects.filter(user=self.request.user)
#
#
# class TestDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = Quiz
#     template_name = 'quiz/quiz/test_detail.html'
#     context_object_name = 'test'
#
#     def get_context_data(self, **kwargs):
#         context = super(TestDetailView, self).get_context_data(**kwargs)
#         pk = self.kwargs['pk']
#         context['questions'] = Question.objects.filter(test=pk)
#         return context
#
#     def test_func(self):
#         test = self.get_object()
#         return self.request.user == test.user
#
#
# class TestCreateView(LoginRequiredMixin, CreateView):
#     model = Test
#     template_name = 'quiz/quiz/test_create.html'
#     context_object_name = 'test'
#     fields = ['title', 'description']
#
#     # Sets the current user = to the 'Test' user field
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#
#
# class TestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Test
#     template_name = 'quiz/quiz/test_update.html'
#     fields = ['title', 'description']
#     context_object_name = 'test'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#
#     def test_func(self):
#         test = self.get_object()
#         return self.request.user == test.user
#
#
# class TestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Test
#     template_name = 'quiz/quiz/test_delete.html'
#     context_object_name = 'test'
#
#     def get_success_url(self):
#         return reverse('quiz:test_list')
#
#     def test_func(self):
#         test = self.get_object()
#         return self.request.user == test.user
