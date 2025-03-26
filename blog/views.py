from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
import logging

logger = logging.getLogger(__name__)

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            logger.error(f"Error creating post: {str(exc)}")
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

def home_view(request):
    return render(request, 'auth.html')

def blog_view(request):
    return render(request, 'blog.html')