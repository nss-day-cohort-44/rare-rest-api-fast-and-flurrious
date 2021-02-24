"""View module for handling requests about profiles"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from djangorarapi.models import Rareuser

class Profiles(ViewSet):
    """Django Rare Profiles View Set"""

    def list(self, request):
        """Handles get all profiles from the database"""

        profiles = Rareuser.objects.all()

        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single profile

        Returns:
            Response -- JSON serialized profile instance
        """

        try:
            # Finds the user from primay key (token) provided in the URL
            user = User.objects.get(auth_token=pk)

            # Finds the Rareuser from the user
            profile = Rareuser.objects.get(user=user)

            serializer = ProfileSerializer(profile, context={'request': request}) 
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def update(self, request, pk=None):

        user = User.objects.get(pk=pk)

        profile = Rareuser.objects.get(user=user)

        profile.bio = request.data['bio']
        profile.profile_image = request.data['profileImage']

        
        profile.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rareuser
        fields = ('bio', 'profile_image', 'created_on')