from django.urls import path
from social_media.views import twitter_view

app_name = 'twitter'
urlpatterns = [
    path('spider-list/', twitter_view.TwitterSpiderListView.as_view(), name='spider-list'),
    path('spider-detail/<int:pk>/', twitter_view.TwitterSpiderDetailView.as_view(), name='spider-detail'),
    path('spider-create/', twitter_view.TwitterSpiderCreateView.as_view(), name='spider-create'),
    path('spider-update/<int:pk>/', twitter_view.TwitterSpiderUpdateView.as_view(), name='spider-update'),
    path('spider-delete/<int:pk>/', twitter_view.TwitterSpiderDeleteView.as_view(), name='spider-delete'),
    path('index/<int:pk>/', twitter_view.index, name='index'),
    path('download-followers/<int:pk>/', twitter_view.download_followers, name='download-followers'),
    path('download-following/<int:pk>/', twitter_view.download_following, name='download-following'),
    path('download-posts/<int:pk>/', twitter_view.download_posts, name='download-posts'),
]
