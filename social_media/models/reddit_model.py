from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import models
import praw
import json
import csv

from social_media.exceptions import InvalidCredentialsError
from social_media.utils.reddit_utils import GetRedditData
from social_media.validators import validate_dictionary_from_json


class RedditApiKey(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	email = models.EmailField()

	api_key = models.CharField(max_length=250)
	api_secret = models.CharField(max_length=250)

	password = models.CharField(max_length=250)
	user_agent = models.CharField(max_length=250)
	username = models.CharField(max_length=250)

	def __str__(self):
		return self.user.username

	def get_api(self):
		api = praw.Reddit(client_id=self.api_key,
						  client_secret=self.api_secret,
						  password=self.password,
						  user_agent=self.user_agent,
						  username=self.username)
		return api

	def save(self, *args, **kwargs):
		try:
			api = self.get_api()
		except:
			raise InvalidCredentialsError
		super(RedditApiKey, self).save(*args, **kwargs)


class RedditSpider(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	reddit_user = models.CharField(max_length=20)

	user_info = models.TextField(default='', blank=True, null=True, validators=[validate_dictionary_from_json])

	def __str__(self):
		return self.reddit_user

	def save(self, *args, **kwargs):
		api = get_object_or_404(RedditApiKey, user=self.user.pk)
		api = api.get_api()
		spider = GetRedditData(api, str(self.reddit_user))

		self.user_info = json.dumps(spider.get_user_information())

		super(RedditSpider, self).save(*args, **kwargs)
