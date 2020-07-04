from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json

from social_media.models.reddit_model import RedditSpider

BASE_TEMPLATE = 'social_media/reddit_templates/reddit_spider/'
BASE_REVERSE = 'social_media:reddit:'


class RedditSpiderListView(LoginRequiredMixin, ListView):
    model = RedditSpider
    template_name = BASE_TEMPLATE + 'spider_list.html'
    context_object_name = 'spiders'
    ordering = ['-date_created']

    def get_queryset(self):
        return RedditSpider.objects.filter(user=self.request.user)


class RedditSpiderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = RedditSpider
    template_name = BASE_TEMPLATE + 'spider_detail.html'
    context_object_name = 'spider'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_info'] = json.loads(self.get_object().user_info)
        return context

    def test_func(self):
        spider = RedditSpider.objects.get(pk=self.kwargs['pk'])
        return self.request.user == spider.user


class RedditSpiderCreateView(LoginRequiredMixin, CreateView):
    model = RedditSpider
    template_name = BASE_TEMPLATE + 'spider_create.html'
    fields = ['reddit_user']
    context_object_name = 'spider'

    def get_success_url(self):
        return reverse(BASE_REVERSE + 'spider-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RedditSpiderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RedditSpider
    template_name = BASE_TEMPLATE + 'spider_update.html'
    fields = ['blog_name']
    context_object_name = 'spider'

    def get_success_url(self):
        return reverse(BASE_REVERSE + 'spider-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        spider = self.get_object()
        return self.request.user == spider.user


class RedditSpiderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RedditSpider
    template_name = BASE_TEMPLATE + 'spider_delete.html'
    context_object_name = 'spider'

    def get_success_url(self):
        return reverse(BASE_REVERSE + 'spider-list')

    def test_func(self):
        spider = self.get_object()
        return self.request.user == spider.user
