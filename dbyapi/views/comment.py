"""View module for handling requests about comments"""
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from dbyapi.models import Comment, Post, DiyUser
from django.core.exceptions import ValidationError


class CommentView(ViewSet):
    """One Comment"""

    def retrieve(self, request, pk=None):
        """Handle GET request for single comment
        Returns: Response -- JSON serialized comment"""

        try:
            comment = Comment.object.get(pk=pk)
            serializer = CommentSerializer(
                comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

        def list(self, request):
            """Handle GET requests to get all comments
            Returns: Response -- JSON serialized list of comments"""

            comments = Comment.objects.all()

            # 'many=True" argument is needed when you are serializing
            # a list of objects instead of a single object.
            serializer = CommentSerializer(
                comments, many=True, context={'request': request})
            return Response(serializer.data)

        def create(self, request):
            """Handle POST operations for comments
            Returns: Response -- JSON serialized comment instance"""

            user = DiyUser.objects.get(user=request.auth.user)
            post = Post.objects.get(pk=request.data['post'])

            comment = Comment()
            comment.user = user
            comment.content = request.data['content']
            comment.date = request.data['date']
            comment.post = post
            comment.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        def update(self, request, pk=None):
            """Handle PUT requests for a comment
            Returns: Response -- Empty body with 204 status code"""
            user = DiyUser.objects.get(user=request.auth.user)
            post = Post.objects.get(pk=request.data['post'])

            comment = Comment.objects.get(pk=pk)
            comment.user = user
            comment.content = request.data['content']
            comment.post = post
            comment.save()
            # 204 status code means everything worked but the server
            # is not sending back any data in the response
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        def destroy(self, request, pk=None):
          """Handle DELETE requests for a single comment
          Returns: Response -- 200, 204, or 500 status code"""

          try:
            comment = Comment.objects.get(pk=pk)
            if comment.user == DiyUser.objects.get(user=request.auth.user):
              comment.delete()
              return Response({}, status=status.HTTP_204_NO_CONTENT)

          except comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

          except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentSerializer(serializers.ModelSerializer):
  """JSON serializer for comments
  Arguments: serializers"""

  class Meta:
    model = Comment
    fields = ('id', 'content', 'date', 'post', 'user')
    depth = 3


class PostSerializer(serializers.ModelSerializer):
  """JSON serializer for posts
  Arguments: serializers"""

  class Meta:
    model = Post
    firleds = ('id', 'category', 'title', 'content', 'image', 'date', 'user')


class CommentUserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ['firstname', 'lastname', 'email']


class CommentDiyUserSerializer(serializers.ModelSerializer):

  user = CommentUserSerializer(many=False)