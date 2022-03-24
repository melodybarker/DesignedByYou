from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.utils.timezone import make_aware
from datetime import datetime
from dbyapi.models import Post, DiyUser, Category, Comment


class PostView(ViewSet):
    """User can see post information"""

    def create(self, request):
        """Hanlde POST operations for post
        Returns: Response -- JSON serialized post instance"""

        diyuser = DiyUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data['category'])

        post = Post()
        post.category = category
        post.title = request.data['title']
        post.content = request.data['content']
        post.image = request.data['image_url']
        post.diyuser = diyuser

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all post
        Returns: Response -- JSON serialized list of posts"""

        posts = Post.objects.all()

        # if diyuser is not None:
        #     posts = posts.filter(diyuser_id=diyuser)

        # if category is not None:
        #     posts = posts.filter(categroy__id=category)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)


    def update(self, request, pk=None):
        """Handle PUT requests for a game
        Returns: Response -- Empty body with 204 status code"""

        diyuser = DiyUser.objects.get(pk=request.data['diyuser'])
        category = Category.objects.get(pk=request.data['category'])

        post = Post.objects.get(pk=pk)
        post.category = category
        post.title = request.data['title']
        post.content = request.data['content']
        post.image_url = request.data['image_url']
        post.diyuser = diyuser
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
            return Response({'message': ex.args[0]},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PostDiyUserSerializer(serializers.ModelSerializer):

    user = PostUserSerializer(many=False)

    class Meta:
        model = DiyUser
        fields = ['id', 'user', 'bio', 'image_url']
        depth = 1


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'label']


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments
    Arguments: serializers"""

    class Meta:
        model = Comment
        fields = ('id', 'content', 'date', 'post', 'diyuser')
        depth = 1


class PostSerializer(serializers.ModelSerializer):

    diyuser = PostDiyUserSerializer(many=False)
    category = CategorySerializer(many=False)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'diyuser', 'title', 'category',
                  'date', 'image_url', 'content', 'comments')
        depth = 3
