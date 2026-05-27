from django.shortcuts import render, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser, OneTimePassword, BlogPost, Comments
from rest_framework import generics, status, mixins, viewsets
from rest_framework.views import APIView
from .serializers import RegisterSerializer, VerifyEmailSerializer, MyTokenObtainPairSerializer, PostSerializer, CommentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
from django.http import HttpResponse
from .utils import async_send_otp
from .permissions import IsAuthor

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#Register User
# class RegisterView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     permission_classes = [AllowAny]
#     serializer_class = RegisterSerializer


class UserRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data
        # try:
        #     async_send_otp(email=user['email'])
        # except:
        #     pass
        return Response(
            {
                'message': f'Your registration was successful'
            }, status=status.HTTP_200_OK
        )
    
class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer


    def post(self, request):
        code = request.data.get('otp_code')
        try:
            user_code_object = OneTimePassword.objects.get(otp_code=code)
            user = user_code_object.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response(
                    {
                        'message': 'Your account has been verified. You can now log in'
                    }, status=status.HTTP_201_CREATED
                )
        except OneTimePassword.DoesNotExist:
            return Response(
                {
                    'message': 'Invalid Otp code or user is already verified'
                }, status=status.HTTP_400_BAD_REQUEST                
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {
                    'message':'You have been logged out successfully'
                }, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view
    
    def get(self, request):
        return Response({
            'message': f'Hello {request.user.username}'  # Greet the authenticated user
        })


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        data = {
            'title':title,
            'content':content
        }
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    #permission_classes = [IsAuthenticated]

class PostListView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    #permission_classes = [IsAuthenticated]


class PostDetailView(generics.RetrieveDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer
    #permission_classes = [IsAuthenticated]


class MyPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)
    

class UpdateBlogPost(generics.UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


class DeleteBlogPost(generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

#Comments
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comments.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = BlogPost.objects.get(id=post_id)
        serializer.save(post=post)


# def delete_view(request):
#     CustomUser.objects.all().delete()
#     return HttpResponse('Users deleted successfully')

# def view_users(request):
#     return CustomUser.objects.all()