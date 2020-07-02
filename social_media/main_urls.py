from django.urls import path, include

app_name = 'social_media'
urlpatterns = [
    path('twitter/', include('social_media.urls.twitter_urls')),
]
