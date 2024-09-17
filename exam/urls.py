from django.urls import path, include
from rest_framework.routers import DefaultRouter

from exam.view import (
    AnswerListView,
    AnswerDetailView,
    QuestionListView,
    QuestionDetailView,
    QuizzesListView,
    QuizzesDetailView,
    NewsListView,
    NewsDetailView,
    AdditionViewSet, CheckAnswersView, CommentaryViewSet, OrderViewSet
)
router = DefaultRouter()
router.register(r'additions', AdditionViewSet, basename='addition')
router.register(r'quizzes/(?P<quiz_pk>\d+)/commentaries', CommentaryViewSet, basename='commentary')
router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('answers/', AnswerListView.as_view(), name='answer-list'),
    path('answers/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('quizzes/', QuizzesListView.as_view(), name='quizzes-list'),
    path('quizzes/<int:pk>/', QuizzesDetailView.as_view(), name='quizzes-detail'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('quizzes/<int:quiz_id>/check-answers/', CheckAnswersView.as_view(), name='check-answers'),

]
