from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/social/', include('allauth.socialaccount.urls')),
    path('register/', views.UserRegisterView.as_view(), name='auth_register'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('create-post/', views.CreatePostView.as_view(), name='create-post'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('my-posts/', views.MyPostsView.as_view(), name='my-posts'),
    path('posts/<int:post_id>/comments/', views.CommentList.as_view(), name='post-comments'),
    path('update-blogpost/<int:pk>/', views.UpdateBlogPost.as_view(), name='update-blogpost'),
    path('delete-blogpost/<int:pk>/', views.DeleteBlogPost.as_view(), name='delete-blogpost'),


    # path('delete/', views.delete_view, name='delete'),
    # path('view-users/', views.view_users, name='delete'),
]

