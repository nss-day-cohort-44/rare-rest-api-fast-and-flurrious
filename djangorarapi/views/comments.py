import json
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from djangorarapi.models import Comment

class Comments(ViewSet):


 def list(self, request):
        """Handle GET requests to comment resource

        Returns:
            Response -- JSON serialized list of comment
        """
        # Get all comments records from the database
        comment = Comment.objects.all()

        # Support filtering comment by post
        #    http://localhost:8000/comment?post=1
        #
        # That URL will retrieve all tabletop comment
        post = self.request.query_params.get('post', None)
        if post is not None:
            comment = comment.filter(post__id=post)

        

        serializer = CommentSerializer(
            comment, many=True, context={'request': request})
        return Response(serializer.data)


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comment

    Arguments:
        serializer type
    """
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content',
                  'created_on')
       