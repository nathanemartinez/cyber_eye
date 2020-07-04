from django.urls import path
from social_media.views import tumblr_view

app_name = 'tumblr'
urlpatterns = [
    path('spider-list/', tumblr_view.TumblrSpiderListView.as_view(), name='spider-list'),
    path('spider-detail/<int:pk>/', tumblr_view.TumblrSpiderDetailView.as_view(), name='spider-detail'),
    path('spider-create/', tumblr_view.TumblrSpiderCreateView.as_view(), name='spider-create'),
    path('spider-update/<int:pk>/', tumblr_view.TumblrSpiderUpdateView.as_view(), name='spider-update'),
    path('spider-delete/<int:pk>/', tumblr_view.TumblrSpiderDeleteView.as_view(), name='spider-delete'),
]
