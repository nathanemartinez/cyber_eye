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
    path('read-followers/<int:pk>/', twitter_view.read_followers, name='read-followers'),
    path('read-following/<int:pk>/', twitter_view.read_following, name='read-following'),
]
