from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json
import time

from social_media.models.twitter_model import TwitterSpider, DummyModel, TwitterApiKey
from social_media.tasks import add, get_followers_or_following, get_infoo, get_picss
from social_media.utils.twitter_utils import GetTwitterData


def index(request, pk):
    add(1, pk)
    obj = DummyModel.objects.get(id=pk)
    return HttpResponse(f"done: {obj.integer}")


class TwitterSpiderListView(LoginRequiredMixin, ListView):
    model = TwitterSpider
    template_name = 'social_media/twitter_templates/twitter_spider/spider_list.html'
    context_object_name = 'spiders'
    ordering = ['-date_created']

    def get_queryset(self):
        return TwitterSpider.objects.filter(user=self.request.user)


class TwitterSpiderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = TwitterSpider
    template_name = 'social_media/twitter_templates/twitter_spider/spider_detail.html'
    context_object_name = 'spider'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_object().no_info():
            pass
        else:
            context['user_info'] = json.loads(self.get_object().user_info)
            context['user_profile_pics'] = json.loads(self.get_object().user_profile_pictures)

        return context

    def test_func(self):
        spider = TwitterSpider.objects.get(pk=self.kwargs['pk'])
        return self.request.user == spider.user


class TwitterSpiderCreateView(LoginRequiredMixin, CreateView):
    model = TwitterSpider
    template_name = 'social_media/twitter_templates/twitter_spider/spider_create.html'
    fields = ['twitter_user']
    context_object_name = 'spider'

    def get_success_url(self):
        return reverse('social_media:twitter:spider-detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        api = TwitterApiKey.objects.first()
        api = api.get_api()
        form = self.get_form()
        if form.is_valid():
            twitter_user = form.cleaned_data['twitter_user']
            form.instance.user = self.request.user
            form.save()
            pk = form.instance.pk
            spider = GetTwitterData(api, str(twitter_user))
            get_infoo(spider, self.request.user, twitter_user, pk)
            get_picss(spider, self.request.user, twitter_user, pk)
            get_followers_or_following(spider, self.request.user, twitter_user, 2)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class TwitterSpiderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TwitterSpider
    template_name = 'social_media/twitter_templates/twitter_spider/spider_update.html'
    fields = ['twitter_user']
    context_object_name = 'spider'

    def get_success_url(self):
        return reverse('social_media:twitter:spider-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        spider = self.get_object()
        return self.request.user == spider.user


class TwitterSpiderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TwitterSpider
    template_name = 'social_media/twitter_templates/twitter_spider/spider_delete.html'
    context_object_name = 'spider'

    def get_success_url(self):
        return reverse('social_media:twitter:spider-list')

    def test_func(self):
        spider = self.get_object()
        return self.request.user == spider.user


