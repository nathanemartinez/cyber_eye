from django.urls import path
from social_media.views import reddit_view

app_name = 'reddit'
urlpatterns = [
    path('spider-list/', reddit_view.RedditSpiderListView.as_view(), name='spider-list'),
    path('spider-detail/<int:pk>/', reddit_view.RedditSpiderDetailView.as_view(), name='spider-detail'),
    path('spider-create/', reddit_view.RedditSpiderCreateView.as_view(), name='spider-create'),
    path('spider-update/<int:pk>/', reddit_view.RedditSpiderUpdateView.as_view(), name='spider-update'),
    path('spider-delete/<int:pk>/', reddit_view.RedditSpiderDeleteView.as_view(), name='spider-delete'),
]
