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

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        comment = Comment.objects.get(pk=pk)

        author = Rareuser.objects.get(user=request.auth.user)
        comment.author = author

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        comment.content = request.data["content"]

        post = Post.objects.get(pk=request.data["post"])
        comment.post = post
        comment.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

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
            serializer = CommentSerializer(
                comment, context={'request': request})
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
        post = self.request.query_params.get('post_id', None)
        if post is not None:
            comment = comment.filter(post__id=post)

        serializer = CommentSerializer(
            comment, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single comment

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:

            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comment

    Arguments:
        serializer type
    """
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content',
                  'created_on')
