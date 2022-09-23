from django.urls import path, include

from api_v2.views import ArticleView

app_name = 'api_v2'

urls_articles = [

]

urlpatterns = [
    path('articles/', ArticleView.as_view()),
    path('articles/<int:pk>/', ArticleView.as_view())


]
