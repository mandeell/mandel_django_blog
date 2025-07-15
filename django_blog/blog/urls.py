from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog views
    path('', views.PostListView.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('author/<int:author_id>/', views.AuthorPostsView.as_view(), name='author_posts'),
    path('tag/<slug:slug>/', views.TagPostsView.as_view(), name='tag_posts'),
    path('search/', views.SearchView.as_view(), name='search'),
    
    # AJAX views
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('comment/', views.CommentCreateView.as_view(), name='add_comment'),
]