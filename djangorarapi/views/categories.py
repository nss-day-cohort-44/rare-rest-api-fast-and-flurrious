"""View module for handling requests about categories"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from djangorarapi.models import Category


class Categories(ViewSet):
    """Rare Categories"""


    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of categories
        """
        # Get all category records from the database
        categories = Category.objects.all()


        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializer type
    """
    class Meta:
        model = Category
        fields = ('id', 'label')