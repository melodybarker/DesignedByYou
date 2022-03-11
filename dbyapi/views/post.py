from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.utils.timezone import make_aware
from datetime import datetime
from dbyapi.models import Post, DiyUser, Category, Comment, Like


class PostView(ViewSet):
  """One Post"""

  def create(self, request):
    """Hanlde POST operations for post
    Returns: Response -- JSON serialized post instance"""

    user = DiyUser.objects.get(user=request.auth.user)
    category = Category.objects.get(pk=request.data['category'])

    post = Post()
    post.category = category
    post.title = request.data['title']
    post.content = request.datat['content']
    post.image = request.data['image']
    post.user = user

    try:
      post.save()
      serializer = PostSerializer(post, context={'request': request})
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as ex:
      return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, reqquest, pk=None):
      """Handle GET requests for single post
      Returns: Response -- JSON serialized post"""

      try:
        post = Post.objects.get(pk=pk)
        serailizer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)
      except Exception as ex:
        return HttpResponseServerError(ex)

    def list(self, request):
      """Handle GET requests to get all post
      Returns: Response -- JSON serialized list of posts"""

      posts = Post.objects.all()
      user = self.request.query_params.get('user_id', None)
      if user is not None:
        posts = posts.filter(user_id=user)

      category = self.request.query_params.get('category_id', None)
      if category is not None:
        posts = posts.filter(categroy__id=type)

      serializer = PostSerializer(posts, many=True, context={'request': request})
      return Response(serializer.data)


    def update(self, request, pk=None):
      """Handle PUT requests for a game
      Returns: Response -- Empty body with 204 status code"""

      user = DiyUser.objects.get(user=request.auth.user)
      category = Category.objects.get(pk=request.data['categroy_id'])

      post = Post.objects.get(pk=pk)
      post.category = category
      post.title = request.data['title']
      post.content = request.data['content']
      post.image = request.data['image']
      post.user = user
      post.save()

      return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
      """Handle DELETE requets for a single post
      Returns: Response -- 200, 404, or 500 status code"""

      try:
        post = Post.objects.get(pk=pk)
        post.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

      except Post.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404)
      except Exception as ex:
        return Response({'message': ex.args[0]}, satus=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostUserSerializer(serializers.ModelSerializer):

  class Meta:
    model = Userfields = ['firstname', 'lastname', 'email']


class PostDiyUserSerializer(serializers.ModelSerializer):

  user = PostUserSerializer(many=False)

  class Meta:
    model = DiyUser
    fields = ['id', 'user', 'bio']


class CategorySerializer(serializers.ModelSerializer):

  class Meta:
    model = Categoryfields = ['id', 'label']


class CommentSerializer(serializers.ModelSerializer):

  user = PostDiyUserSerializer(many=False)

  class Meta:
    model = Comment
    fields = ('id', 'user', 'content', 'date')


class PostSerializer(serializers.ModelSerializer):

  user = PostDiyUserSerializer(many=False)
  category = CategorySerializer(many=False)
  comment = CommentSerializer(many=False)

  class Meta:
    model = Post
    fields = ('id', 'user', 'title', 'category', 'date', 'image', 'content', 'comment')