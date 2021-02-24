from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from djangorarapi.views import register_user, login_user
from djangorarapi.views import Comments
from djangorarapi.views import Posts, Categories, Comments, Tags, Profiles


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', Categories, 'category')
router.register(r'profiles', Profiles, 'profile')
router.register(r'comments', Comments, 'comment')
router.register(r'posts', Posts, 'post')
router.register(r"tags", Tags, "tag")

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
