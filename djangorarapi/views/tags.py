
from django.http.response import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from djangorarapi.models import Tag

class Tags(ViewSet):
    """Tag view set"""

    def list(self,request):
        """GET all tag object"""
        tags = Tag.objects.all()

        
        serialized_Tags = TagSerializer(tags, many=True, context={'request': request} )
        
        return Response(serialized_Tags.data, status=status.HTTP_200_OK)
        

    def retrieve(self, request, pk=None):
        """Handles get requests for a single tag"""
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST requests for tags"""
        app_user = User.objects.get(id=request.auth.user.id)
        tag = Tag()
        tag.label = request.data["label"]
        tag.author = app_user
        
        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for tags"""
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for tags"""
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({'message':'tag not found'}, status=status.HTTP_404_NOT_FOUND)
        tag.label = request.data["label"]
        tag.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for Tag"""
    class Meta:
        model = Tag
        fields = ('id', 'label')
