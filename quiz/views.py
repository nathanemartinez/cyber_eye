from django.shortcuts import render
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse

from .models import QuizTaker, Test, Question, Answer


class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'quiz/test_list.html'
    context_object_name = 'tests'

    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)


class TestDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Test
    template_name = 'quiz/test_detail.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super(TestDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['questions'] = Question.objects.filter(test=pk)
        return context

    def test_func(self):
        test = self.get_object()
        return self.request.user == test.user


class TestCreateView(LoginRequiredMixin, CreateView):
    model = Test
    template_name = 'quiz/test_create.html'
    context_object_name = 'test'
    fields = ['title', 'description']

    # Sets the current user = to the 'Test' user field
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Test
    template_name = 'quiz/test_update.html'
    fields = ['title', 'description']
    context_object_name = 'test'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        test = self.get_object()
        return self.request.user == test.user


class TestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Test
    template_name = 'quiz/test_delete.html'
    context_object_name = 'test'

    def get_success_url(self):
        return reverse('quiz:test_list')

    def test_func(self):
        test = self.get_object()
        return self.request.user == test.user

