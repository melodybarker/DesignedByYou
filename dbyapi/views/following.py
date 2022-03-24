from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from dbyapi.models import DiyUser, Following, Post
from dbyapi.views.comment import CommentSerializer
from dbyapi.views.post import PostDiyUserSerializer, PostUserSerializer
from dbyapi.views.category import CategorySerializer





class FollowingView(ViewSet):
    """DIY User following"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single diyuser following"""

        try:
            following = Following.objects.get(pk=pk)
            serializer = FollowingSerializer(following, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests for all user's following
        Returns: Response -- JSON serialized list of following"""

        follower = Following.objects.all()
        serializer = FollowingSerializer(follower, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns: Response -- JSON serialized following"""

        to_diyuser = DiyUser.objects.get(pk=request.data['to_diyuser'])
        from_diyuser = DiyUser.objects.get(user=request.auth.user)

        following = Following()
        following.to_diyuser = to_diyuser
        following.from_diyuser = from_diyuser

        try:
            following.save()
            serializer = FollowingSerializer(following, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a sinlge user"""

        try:
            following = Following.objects.get(pk=pk)
            following.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except DiyUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FollowingSerializer(serializers.ModelSerializer):
    """JSON serializer for following"""

    class Meta:
        model = Following
        fields = ('id', 'to_diyuser', 'from_diyuser')
        depth = 3

class FollowingDiyUserSerializer(serializers.ModelSerializer):
    """JSON serializer for diyusers"""

    class Meta:
        model = DiyUser
        fields = ('id', 'user')



class FollowingUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')