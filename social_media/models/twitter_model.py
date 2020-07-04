from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import models
import tweepy
import json
import csv

from social_media.exceptions import InvalidCredentialsError
from social_media.utils.twitter_utils import GetTwitterData
from social_media.validators import validate_dictionary_from_json


class TwitterApiKey(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        super(TwitterApiKey, self).save(*args, **kwargs)


class TwitterSpider(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    twitter_user = models.CharField(max_length=20)

    user_info = models.TextField(default='', blank=True, null=True, validators=[validate_dictionary_from_json])
    user_profile_pictures = models.TextField(default='', blank=True, null=True)

    followers = models.TextField(default='social_media/media/social_media/twitter/followers/default.txt', blank=True, null=True)
    following = models.TextField(default='social_media/media/social_media/twitter/following/default.txt', blank=True, null=True)

    def __str__(self):
        return self.twitter_user

    def _remove_at_sign(self):
        user = self.twitter_user
        if user.startswith('@'):
            return user[1:]
        else:
            return user

    def _get_followers_or_following(self, spider: GetTwitterData, followers: bool):
        if followers:
            info_dict = spider.get_followers(count=10)
            path = f'social_media/media/social_media/twitter/followers/{self.user.username}_{self.twitter_user}_{self.pk}.txt'

        else:
            info_dict = spider.get_following(count=10)
            path = f'social_media/media/social_media/twitter/following/{self.user.username}_{self.twitter_user}_{self.pk}.txt'

        users = [user_obj_list.screen_name for user_obj_list in info_dict]
        with open(path, 'w', newline='') as file:
            for user in users:
                file.write(f'{user}\n')
        return path

    def save(self, *args, **kwargs):
        api = get_object_or_404(TwitterApiKey, user=self.user.pk)
        api = api.get_api()
        spider = GetTwitterData(api, str(self.twitter_user))

        self.user_info = json.dumps(spider.get_user_information())
        self.user_profile_pictures = json.dumps(spider.get_user_profile_banner_urls())

        self.twitter_user = self._remove_at_sign()
        self.followers = self._get_followers_or_following(spider, followers=True)
        self.following = self._get_followers_or_following(spider, followers=False)

        super(TwitterSpider, self).save(*args, **kwargs)


class DummyModel(models.Model):
    integer = models.IntegerField()

    def __str__(self):
        return f'{self.integer}'



