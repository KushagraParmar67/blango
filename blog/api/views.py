from rest_framework import generics, viewsets
from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer, TagSerializer
from blog.models import Post, Tag
from blango_auth.models import User
from blog.api.permissions import AuthorModifyOrReadonly, IsAdminUserForObject
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from rest_framework.exceptions import PermissionDenied




class PostList(generics.ListCreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
  # permission_classes = [AuthorModifyOrReadonly | IsAdminUserForObject] 
  queryset = Post.objects.all()
  serializer_class = PostDetailSerializer

class UserDetail(generics.RetrieveAPIView):
  @method_decorator(cache_page(300))
  def get(self, *args, **kwargs):
        return super(UserDetail, self).get(*args, *kwargs)
  lookup_field = "email"
  queryset = User.objects.all()
  serializer_class = UserSerializer

class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

  @action(methods=["get"], detail=True, name="Posts with the Tag")
  def posts(self, request, pk=None):
    tag = self.get_object()
    post_serializer = PostSerializer(
      tag.posts, many=True, context={'request':request}
    )
    return Response(post_serializer.data)
  @method_decorator(cache_page(300))
  def list(self, *args, **kwargs):
        return super(TagViewSet, self).list(*args, **kwargs)

  @method_decorator(cache_page(300))
  def retrieve(self, *args, **kwargs):
        return super(TagViewSet, self).retrieve(*args, **kwargs)

class PostViewSet(viewsets.ModelViewSet):
  permission_classes = [AuthorModifyOrReadonly | IsAdminUserForObject]
  queryset = Post.objects.all()

  def get_serializer_class(self):
    if self.action in ("list", "create"):
      return PostSerializer
    return PostDetailSerializer
  @method_decorator(cache_page(300))
  @method_decorator(vary_on_headers("Authorization"))
  @method_decorator(vary_on_cookie)
  @action(methods=["get"], detail=False, name='Posts By the logged User')
  def mine(self, request):
    if request.user.is_anonymous:
      raise PermissionDenied("you mush be logged in to see which posts are yours")
    posts = self.get_queryset().filter(author=request.user)
    serializer = PostSerializer(posts, manhy=True, context={"request":request})
    return Response(serializer.data)

  @method_decorator(cache_page(120))
  def list(self, *args, **kwargs):
        return super(PostViewSet, self).list(*args, **kwargs)