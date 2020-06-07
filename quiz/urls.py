from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('tests/', views.TestListView.as_view(), name='test_list'),
    path('test/new/', views.TestCreateView.as_view(), name='test-create'),
    path('test/<int:pk>/', views.TestDetailView.as_view(), name='test-detail'),
    path('test/<int:pk>/update', views.TestUpdateView.as_view(), name='test-update'),
    path('test/<int:pk>/delete', views.TestDeleteView.as_view(), name='test-delete'),
]
