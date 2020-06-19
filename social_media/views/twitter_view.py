from django.shortcuts import render
from django.views.generic import ListView
import tweepy
from tweepy.auth import OAuthHandler
from social_media.models.twitter_model import Tweet


class TweetListView(ListView):
    model = Tweet
    template_name = 'social_media/twitter_templates/tweet_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Tweet.objects.order_by('-published_date')

