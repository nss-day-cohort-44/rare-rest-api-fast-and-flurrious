"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from djangorarapi.models import Post, Rareuser, Category, Tag, Post_Tag
from rest_framework.decorators import action

class Posts(ViewSet):
    #Django Rare Posts View Set

    def list(self, request):
        #Handles get all posts from the database

        posts = Post.objects.all()
        # localhost:8000/posts?user_id=fas'ljfna

        # Looks for the user_id query parameter
        rare_token = self.request.query_params.get('user_id', None)

        # IF the user token in the query exists the below will run
        if rare_token is not None:
            # Finds the user by the authentication token, THEN finds the rare_user from user
            rare_user = Rareuser.objects.get(user = User.objects.get(auth_token=rare_token))
            posts = Post.objects.filter(user=rare_user)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=[ 'post', 'delete'], detail=True)
    def tag(self, request, pk=None):

        if request.method=="POST":
            
            post=Post.objects.get(pk=pk)
            tag=Tag.objects.get(pk=request.data["tagId"])
            try:
                post_tag = Post_Tag.objects.get(post=post, tag=tag)
                return Response(
                    {'message': 'this tag is on the post.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except Post_Tag.DoesNotExist:    
                post_tag=Post_Tag()
                post_tag.post=post
                post_tag.tag=tag
                post_tag.save()
                return Response({}, status=status.HTTP_201_CREATED)

        elif request.method=="DELETE":
            try:
                post=Post.objects.get(pk=pk)

            except Post.DoesNotExist:
                return Response(
                    {'message': 'Post does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # user = RareUser.objects.get(user=request.auth.user)
            try:
                post=Post.objects.get(pk=pk)
                
                tag=Tag.objects.get(pk=request.data["tag_id"])
                
                post_tag = Post_Tag.objects.get(post=post, tag=tag)
                
                post_tag.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Post_Tag.DoesNotExist:
                return Response(
                    {'message': 'tag is not on the post'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post instance
        """

        try: 
            post = Post.objects.get(pk=pk)
            matching_tags = Tag.objects.filter(tags__post=post)
            post.tags=matching_tags

            serializer = PostSerializer(post, context={'request': request}) 
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

        # try:
        #     # `pk` is a parameter to this function, and
        #     # Django parses it from the URL route parameter
        #     #   http://localhost:8000/posts/2
        #     #
        #     # The `2` at the end of the route becomes `pk`
        #     post = Post.objects.get(pk=pk)
        #     serializer = PostSerializer(post, context={'request': request})
        #     return Response(serializer.data)
        # except Exception as ex:
        #     return HttpResponseServerError(ex)
    
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

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ( 'id', 'label' )

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'profile_image_url', 'content', 'approved', 'user', 'category', 'tags')
        depth = 2

# class Post_TagSerializer(serializers.ModelSerializer):
#     """JSON serializer for event organizer"""
#     tag = TagSerializer(many=False)
#     post = PostSerializer(many=False)

#     class Meta:
#         model = Tag
#         fields = ['tag']

