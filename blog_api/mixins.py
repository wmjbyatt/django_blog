from django.contrib.auth.models import AnonymousUser
from django.db.models import Q

from blog_api.models import Post


class PostAuthenticationMixin:
    def get_queryset(self):
        user = self.request.user

        if isinstance(user, AnonymousUser):
            return Post.objects.filter(visibility='PU')
        else:
            return Post.objects.filter(Q(visibility='PU') | Q(user=user))