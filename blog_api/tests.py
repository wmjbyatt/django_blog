"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from blog_api.models import Post
from django.contrib.auth.models import User

class APIIntegrationTests(TestCase):
    def setUp(self):
        # Create test users
        user_1 = User.objects.create(
            username = "user1",
            first_name = "UserOne",
            last_name = "UserOne"
        )

        user_2 = User.objects.create(
            username = "user2",
            first_name = "UserTwo",
            last_name = "UserTwo"
        )

        # Create test posts
        Post.objects.create(
            title = "PUBLIC Post 1",
            visibility = "PU",
            body = "This is the post body",
            user = user_1,
            published_date = "2010-01-01T12:00-05:00"
        )

        Post.objects.create(
            title = "DRAFT Post 1",
            visibility = "DR",
            body = "This is the post body",
            user = user_1,
            published_date = "2011-01-01T12:00-05:00"
        )

        Post.objects.create(
            title = "PUBLIC Post 2",
            visibility = "PU",
            body = "This is the post body",
            user = user_2,
            published_date = "2012-01-01T12:00-05:00"
        )

        Post.objects.create(
            title = "DRAFT Post 2",
            visibility = "DR",
            body = "This is the post body",
            user = user_2,
            published_date = "2013-01-01T12:00-05:00"
        )

    def test_posts_index_get(self):
        """
        Tests that posts index call returns correct values
        """

        expected_body= '[{"id": 3, "published_date": "2012-01-01T17:00:00Z", "user": 2, "title": "PUBLIC Post 2", "body": "This is the post body", "visibility": "PU"}, ' \
                         '{"id": 1, "published_date": "2010-01-01T17:00:00Z", "user": 1, "title": "PUBLIC Post 1", "body": "This is the post body", "visibility": "PU"}]'

        client = Client()
        response = client.get('/api/posts/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected_body)