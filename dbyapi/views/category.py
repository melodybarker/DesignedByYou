from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import ValidationError
from dbyapi.models import Category
from rest_framework import status


class CategoryView(ViewSet):
  """category types"""

  def retrieve(self, request, pk=None):
    """Handle GET requests for single post category

    Returns:
      Response -- JSON serialized post category type
    """
    try:
      category = Category.objects.get(pk=pk)
      serializer = CategorySerializer(
        category, context={'request': request})
      return Response(serializer.data)
    except Exception as ex:
      return HttpResponseServerError(ex)

  def list(self, request):
        """Handle GET requests to get all categories
        Returns: Response -- JSON serialized list of categories
        """
        categories = Category.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    Arguments: serializers"""
    class Meta:
        model = Category
        fields = ('id','label')