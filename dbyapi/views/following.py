from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from dbyapi.models import DiyUser
# from dbyapi.views.diyuser import DiyUserSerializer


class FollowingView(ViewSet):
    """DIY User following"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single diyuser following"""

        try:
            following = DiyUser.objects.get(pk=pk)
            serializer = DiyUserSerializer(following, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests for all user's following
        Returns: Response -- JSON serialized list of following"""

        following = DiyUser.objects.all()
        serializer = DiyUserSerializer(following, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns: Response -- JSON serialized following"""

        following = DiyUser.objects.get(pk=request.data['to_diyuser'])
        follower = DiyUser.objects.get(user=request.auth.user)

        diyuser = DiyUser()
        diyuser.to_diyuser = following
        diyuser.from_diyuser = follower

        try:
            diyuser.save()
            serializer = DiyUserSerializer(diyuser, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a sinlge user"""

        try:
            following = DiyUser.objects.get(pk=pk)
            following.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except DiyUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DiyUserSerializer(serializers.ModelSerializer):
    """JSON serializer for following"""

    class Meta:
        model = DiyUser
        fields = ('id', 'following', 'likes', 'user', 'image_url', 'created_on', 'bio')