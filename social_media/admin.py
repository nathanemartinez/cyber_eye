from django.contrib import admin
from social_media.models.twitter_model import ApiKey, TwitterSpider

# Twitter
admin.site.register(ApiKey)
admin.site.register(TwitterSpider)
