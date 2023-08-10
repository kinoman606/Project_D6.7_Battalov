from django.urls import path
from .views import *


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('authors', AuthorList.as_view(), name='author_list'),
   path('search/', SearchList.as_view(), name='search_list'),
   path('news/', NewsList.as_view(), name='news_list'),
   path('article/', ArticleList.as_view(), name='article_list'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit', PostEdit.as_view(), name='news_edit'),
   path('<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit', PostEdit.as_view(), name='article_edit'),
   path('article/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
   path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
]