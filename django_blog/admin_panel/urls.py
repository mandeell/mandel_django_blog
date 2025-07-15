from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Posts management
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Comments moderation
    path('comments/', views.CommentListView.as_view(), name='comment_list'),
    path('comments/<int:pk>/approve/', views.CommentApproveView.as_view(), name='comment_approve'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    
    # Tags management
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/create/', views.TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:pk>/edit/', views.TagUpdateView.as_view(), name='tag_edit'),
    path('tags/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),
    
    # User management
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    
    # Subscribers management
    path('subscribers/', views.SubscriberListView.as_view(), name='subscriber_list'),
    path('subscribers/<int:pk>/delete/', views.SubscriberDeleteView.as_view(), name='subscriber_delete'),
    path('subscribers/email/', views.SubscriberEmailView.as_view(), name='subscriber_email_all'),
    path('subscribers/<int:pk>/email/', views.SubscriberEmailView.as_view(), name='subscriber_email'),
]