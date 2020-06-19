from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.db import models

from social_media.exceptions import InvalidCredentialsError

import tweepy

consumer_key = 'fMISBFv6yEuCATuDx2lMWc62n'
consumer_secret = 'LAqDJileJeEeFmQUf7KtWEcKTpyjqF3hatb9fha04XNWDSPlky'
access_token = '1089278284318142464-SLCYIOcKmuOymXnn4ESXslFNFH35U2'
access_token_secret = '159AL0xv2al4J2ZlfRVEHu5NYgDL8Bzh3jUdVyHBrp8uU'


class ApiKey(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()

    api_key = models.CharField(max_length=250)
    api_secret = models.CharField(max_length=250)

    access_token = models.CharField(max_length=250)
    access_token_secret = models.CharField(max_length=250)

    def __str__(self):
        return self.user.username

    def get_api(self):
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api

    def save(self, *args, **kwargs):
        # Verify credentials
        api = self.get_api()
        try:
            api.verify_credentials()
        except tweepy.TweepError:
            raise InvalidCredentialsError

        super(ApiKey, self).save(*args, **kwargs)


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=250, null=True, blank=True)
    tweet_text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tweet_text

