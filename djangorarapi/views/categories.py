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
    def create(self, request):
        # handle POST HTTP method, return HTTP status of 201 for success
        category = Category()
        category.label = request.data["label"]

        # Try to save new category to the database, then
        # serialize the category instance as JSON, and send the
        # JSON as a response to the client request
        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # catch any exceptions from the above save or serialzier calls
        except ValidationError as ex:
            return Response ({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


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