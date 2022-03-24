from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from dbyapi.models import DiyUser, Post, Like


class LikesView(ViewSet):
    """Likes"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single user's likes"""

        try:
            liker = Like.objects.get(pk=pk)
            serializer = LikeSerializer(liker, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests for all user's likes"""

        likers = Like.objects.all()
        serializer = LikeSerializer(likers, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns: Response -- JSON serialized likes"""

        liker = DiyUser.objects.get(user=request.auth.user)
        diypost = Post.objects.get(pk=request.data['diypost'])

        likes = Like()
        likes.liker = liker
        likes.diypost = diypost

        try:
            likes.save()
            serializer = LikeSerializer(likes, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a sinlge like post"""

        try:
            liker = Like.objects.get(pk=pk)
            liker.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except DiyUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'liker', 'diypost')
        depth = 3
class LikeDiyUserSerializer(serializers.ModelSerializer):
    """JSON serializer for liker"""

    class Meta:
        model = DiyUser
        fields = ('id', 'user')
        depth = 3


class LikePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('__all__')
        depth=3

class LikeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')