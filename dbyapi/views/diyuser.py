
"""View module for handling requests about diyusers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dbyapi.models import DiyUser


class DiyUserView(ViewSet):
  """One DiyUser"""

  def retrieve(self, request, pk=None):
    """Handle GET requests for single diyuser
    Return: Response -- JSON serialized diyuser"""

    try:
      diyuser = DiyUser.objects.get(pk=pk)
      serializer = DiyUserSerializer(diyuser, context={'request': request})
      return Response(serializer.data)
    except Exception as ex:
      return HttpResponseServerError(ex)

  def list(self, request):
    """Handle GET requests to get all diyusers
    Returns: Response -- JSON serialized list of diyusers"""

    diyusers = DiyUser.objects.all()

    serializer = DiyUserSerializer(
      diyusers, many=True, context={'request': request})
    return Response(serializer.data)


class DiyUserSerializer(serializers.ModelSerializer):
  """JSON serializer for diyusers
  Arugments: serializers"""

  class Meta:
    model = DiyUser
    fields = ('id', 'user', 'bio')
    depth = 3