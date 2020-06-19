from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('test/<int:pk>/', views.TakeQuiz.as_view(), name='take-quiz'),

    # path('tests/', views.TestListView.as_view(), name='test_list'),
    # path('test/new/', views.TestCreateView.as_view(), name='test-create'),
    # path('test/<int:pk>/', views.TestDetailView.as_view(), name='test-detail'),
    # path('test/<int:pk>/update/', views.TestUpdateView.as_view(), name='test-update'),
    # path('test/<int:pk>/delete/', views.TestDeleteView.as_view(), name='test-delete'),
    # path('test/<int:pk>/take/', views.TestTake.as_view(), name='test-take'),
    # path('testing/<int:question_pk>/', views.answer_question, name='answer_question'),
    # path('testing/take/<int:pk>/', views.TakeTheTest.as_view(), name='take_the_test'),
    # path('quiz/take/<int:quiz>/question/<int:pk>/', views.TakeQuiz.as_view(), name='take-quiz'),
]
