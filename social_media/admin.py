from django.contrib import admin
from social_media.models.twitter_model import ApiKey, Tweet

# Twitter
admin.site.register(ApiKey)
admin.site.register(Tweet)
