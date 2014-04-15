# Create your views here.
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from blog_api.models import Post

from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from blog_api.serializers import UserSerializer, PostSerializer
from blog_api.mixins import PostAuthenticationMixin

class UsersView(generics.ListCreateAPIView):
    model = User
    serializer_class = UserSerializer


class UserView(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer


class PostsView(PostAuthenticationMixin, generics.ListCreateAPIView):
    serializer_class = PostSerializer

class PostsByUserView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        userid = self.kwargs.get('user_pk')
        posts = Post.objects.filter(user=userid)

        if userid == str(self.request.user.id):
            return posts

        return posts.filter(visibility = 'PU')


class PostView(generics.RetrieveUpdateDestroyAPIView, PostAuthenticationMixin):
    serializer_class = PostSerializer

class SessionView(APIView):
    permission_classes = (permissions.AllowAny,)

    error_messages = {
        'invalid': "Invalid username or password",
        'disabled': "Sorry, this account is suspended",
    }

    def _error_response(self, message_key):
        data = {
            'success': False,
            'message': self.error_messages[message_key],
            'user_id': None,
        }
        return Response(data)

    def get(self, request, *args, **kwargs):
        # Get the current user
        if request.user.is_authenticated():
            return Response({'user_id': request.user.id})
        return Response({'user_id': None})

    def post(self, request, *args, **kwargs):
        # Login
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'success': True, 'user_id': user.id})
            return self._error_response('disabled')
        return self._error_response('invalid')

    def delete(self, request, *args, **kwargs):
        # Logout
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

