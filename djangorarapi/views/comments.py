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
from djangorarapi.models import Comment, Rareuser, Post

class Comments(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized comment instance
        """

        comment = Comment()
        # Uses the token passed in the `Authorization` header
        author = Rareuser.objects.get(user=request.auth.user)
        comment.author = author

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        comment.content = request.data["content"]
        comment.created_on = request.data["created_on"]


        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `post` in the body of the request.
        post = Post.objects.get(pk=request.data["post"])
        comment.post = post
        

        # Try to save the new comment to the database, then
        # serialize the comment instance as JSON, and send the
        # JSON as a response to the client request
        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
   


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
       