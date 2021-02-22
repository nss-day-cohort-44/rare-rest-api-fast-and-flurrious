"""View module for handling requests about games"""
from djangorarapi.models.categories import Category
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from djangorarapi.models import Post, Rareuser, Category
from django.contrib.auth.models import User

class Posts(ViewSet):
    #Django Rare Posts View Set

    def list(self, request):
        #Handles get all posts from the database

        posts = Post.objects.all()
        # localhost:8000/posts?user_id=fas'ljfna

        rare_token = self.request.query_params.get('user_id', None)
        rare_user = Rareuser.objects.get(user = User.objects.get(auth_token=rare_token))
        print(rare_user)
        if rare_token is not None:
            posts = Post.objects.filter(user=rare_user)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        
        rare_user = Rareuser.objects.get(user=request.auth.user)

        post = Post()
        post.title = request.data["title"]
        post.profile_image_url = request.data["profileImageUrl"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.user = rare_user

        category = Category.objects.get(pk=request.data["categoryId"])

        post.category = category

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def update(self, request, pk=None):
        user = Rareuser.objects.get(user=request.auth.user)

        post = Post.objects.get(pk=pk)
        post.title = request.data['title']
        post.profile_image_url = request.data['profileImageUrl']
        post.content = request.data['content']
        post.approved = request.data['approved']
        post.user = user

        category = Category.objects.get(pk=request.data['categoryId'])
        post.category = category
        
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'profile_image_url', 'content', 'approved', 'user', 'category')
        depth = 1