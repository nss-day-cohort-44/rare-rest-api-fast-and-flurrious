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

    def update(self, reqeust, pk=None):
        # Handle PUT request for a category, return HTTP status code of 204 upon success
        category = Category.objects.get(pk=pk)
        category.label = reqeust.data["label"]
        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    # Handle HTTP DELETE method and return HTTP status code of 204, 404, or 500
    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            #return HTTP 204 to client if no errors
            return Response({}, status=status.HTTP_204_NO_CONTENT)

       # return HTTP 404 to client if label not found
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        # return HTTP 500 to client if exception is thrown
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        





class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializer type
    """
    class Meta:
        model = Category
        fields = ('id', 'label')