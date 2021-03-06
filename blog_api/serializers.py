from blog_api.models import Post
from django.contrib.auth.models import User
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ('id', 'published_date', 'user', 'title', 'body', 'visibility')

class UserSerializer(serializers.ModelSerializer):
  posts = serializers.RelatedField(many = True)

  class Meta:
    model = User
    fields = ('id', 'username', 'first_name', 'last_name', 'posts')

