from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json

from social_media.models.tumblr_model import TumblrSpider

BASE_TEMPLATE = 'social_media/tumblr_templates/tumblr_spider/'


class TumblrSpiderListView(LoginRequiredMixin, ListView):
    model = TumblrSpider
    template_name = BASE_TEMPLATE + 'spider_list.html'
    context_object_name = 'spiders'
    ordering = ['-date_created']

    def get_queryset(self):
        return TumblrSpider.objects.filter(user=self.request.user)


class TumblrSpiderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = TumblrSpider
    template_name = BASE_TEMPLATE + 'spider_detail.html'
    context_object_name = 'spider'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_info'] = json.loads(self.get_object().user_info)
        return context

    def test_func(self):
        spider = TumblrSpider.objects.get(pk=self.kwargs['pk'])
        return self.request.user == spider.user


class TumblrSpiderCreateView(LoginRequiredMixin, CreateView):
    model = TumblrSpider
    template_name = BASE_TEMPLATE + 'spider_create.html'
    fields = ['blog_name']
    context_object_name = 'spider'

    def get_success_url(self):
        return reverse('social_media:tumblr:spider-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TumblrSpiderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TumblrSpider
    template_name = BASE_TEMPLATE + 'spider_update.html'
    fields = ['blog_name']
    context_object_name = 'spider'

    def get_success_url(self):
        return reverse('social_media:tumblr:spider-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        spider = self.get_object()
        return self.request.user == spider.user


class TumblrSpiderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TumblrSpider
    template_name = BASE_TEMPLATE + 'spider_delete.html'
    context_object_name = 'spider'

    def get_success_url(self):
        return reverse('social_media:tumblr:spider-list')

    def test_func(self):
        spider = self.get_object()
        return self.request.user == spider.user
