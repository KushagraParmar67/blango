from rest_framework import generics
from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer
from blog.models import Post
from blango_auth.models import User
from blog.api.permissions import AuthorModifyOrReadonly, IsAdminUserForObject

class PostList(generics.ListCreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [AuthorModifyOrReadonly | IsAdminUserForObject] 
  queryset = Post.objects.all()
  serializer_class = PostDetailSerializer

class UserDetail(generics.RetrieveAPIView):
  lookup_field = "email"
  queryset = User.objects.all()
  serializer_class = UserSerializer