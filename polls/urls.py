from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.QuestionDetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.QuestionResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("create/", views.create_question, name="create-question"),
    path("update/<int:pk>/", views.update_question, name="update-question"),
]
