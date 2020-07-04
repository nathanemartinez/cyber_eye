from django.urls import path, include

app_name = 'social_media'
urlpatterns = [
    path('twitter/', include('social_media.urls.twitter_urls')),
    path('tumblr/', include('social_media.urls.tumblr_urls')),
    path('reddit/', include('social_media.urls.reddit_urls')),
]
