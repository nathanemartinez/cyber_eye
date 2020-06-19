from django.urls import path
from social_media.views import twitter_view

app_name = 'quiz'
urlpatterns = [
    path('test/<int:pk>/', views.TakeQuiz.as_view(), name='take-quiz'),
]
