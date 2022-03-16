"""View module for handling requests about diyusers"""
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dbyapi.models import DiyUser


class DiyUserView(ViewSet):
    """One DiyUser"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single diyuser
        Return: Response -- JSON serialized diyuser"""
        diyuser = request.auth.user.diy_user

        serializer = DiyUserSerializer(diyuser, context={'request': request})
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all diyusers
        Returns: Response -- JSON serialized list of diyusers"""

        diyusers = DiyUser.objects.all()
        serializer = DiyUserSerializer(
            diyusers, many=True, context={'request': request})
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class DiyUserSerializer(serializers.ModelSerializer):
    """JSON serializer for diyusers
    Arugments: serializers"""

    class Meta:
        model = DiyUser
        fields = ('id', 'user', 'bio', 'following', 'likes', 'image_url')
        depth = 3
