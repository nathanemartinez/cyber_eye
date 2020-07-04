from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import models
import pytumblr
import json
import csv

from social_media.exceptions import InvalidCredentialsError
from social_media.utils.tumblr_utils import GetTumblrData
from social_media.validators import validate_dictionary_from_json


class TumblrApiKey(models.Model):
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
		api = pytumblr.TumblrRestClient(
			consumer_key=self.api_key,
			consumer_secret=self.api_secret,
			oauth_token=self.access_token,
			oauth_secret=self.access_token_secret,
		)
		return api

	def save(self, *args, **kwargs):
		try:
			api = self.get_api()
		except:
			raise InvalidCredentialsError
		super(TumblrApiKey, self).save(*args, **kwargs)


class TumblrSpider(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	blog_name = models.CharField(max_length=50)

	user_info = models.TextField(default='', blank=True, null=True, validators=[validate_dictionary_from_json])

	def __str__(self):
		return self.blog_name

	def save(self, *args, **kwargs):
		api = get_object_or_404(TumblrApiKey, user=self.user.pk)
		api = api.get_api()
		spider = GetTumblrData(api, str(self.blog_name))

		self.user_info = json.dumps(spider.get_blog_info())

		super(TumblrSpider, self).save(*args, **kwargs)
