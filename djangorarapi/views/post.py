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

class Posts(ViewSet):
    #Django Rare Posts View Set

    def list(self, request):
        #Handles get all posts from the database

        posts = Post.objects.all()

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        
        rare_user = Rareuser.objects.get(user=request.auth.user)

        post = Post()
        post.title = request.data["title"]
        post.publication_date = request.data["publicationDate"]
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



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'profile_image_url', 'content', 'approved', 'user')
        depth = 1