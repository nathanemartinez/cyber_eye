from django.contrib import admin
from social_media.models.twitter_model import TwitterApiKey, TwitterSpider, DummyModel
from social_media.models.tumblr_model import TumblrApiKey, TumblrSpider
from social_media.models.reddit_model import RedditApiKey, RedditSpider

# Twitter
admin.site.register(TwitterApiKey)
admin.site.register(TwitterSpider)
admin.site.register(DummyModel)

admin.site.register(TumblrApiKey)
admin.site.register(TumblrSpider)

admin.site.register(RedditApiKey)
admin.site.register(RedditSpider)
