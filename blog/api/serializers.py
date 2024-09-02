from rest_framework import serializers
from blog.models import Post, Tag, Comment
from blango_auth.models import User
from versatileimagefield.serializers import VersatileImageFieldSerializer

class PostSerializer(serializers.ModelSerializer):
  tags = serializers.SlugRelatedField(slug_field="value", many=True, queryset=Tag.objects.all())
  author = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name="api_user_detail", lookup_field="email")
  hero_image = VersatileImageFieldSerializer(
        sizes=[
            ("full_size", "url"),
            ("thumbnail", "thumbnail__100x100"),
            ("square_crop", "crop__200x200"),
        ],
        read_only=True,
    )
  class Meta:
    model = Post
    exclude = ["ppoi"]
    readonly = ["modifield_at", "created_at"]

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["first_name", "last_name", "email"]

class TagField(serializers.SlugRelatedField):
  def to_internal_value(self, data):
    try:
      return self.get_queryset().get_or_create(value=data.lower())[0]
    except (TypeError, ValueError):
      self.fail(f"Tag Value {data} is invalid")

class CommentSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(required = False)
  creater = UserSerializer(read_only=True)

  class Meta:
    model = Comment
    fields = ["id", "creater", "content", "modifield_at", "created_at"]
    read_only = ["modifield_at", "created_at"]

class PostDetailSerializer(PostSerializer):
    comments = CommentSerializer(many=True)
    
    def update(self, instance, validated_data):
        comments = validated_data.pop("comments")

        instance = super(PostDetailSerializer, self).update(instance, validated_data)

        for comment_data in comments:
          if comment_data.get("id"):
            continue
          comment = Comment(**comment_data)
          comment.creator = self.context["request"].user 
          comment.content_object = instance
          comment.save()

        return instance

class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = "__all__"