"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from blog_api.models import Post
from django.contrib.auth.models import User



class AbstractAPIDataTests(TestCase):
    def setUp(self):
         # Create test users
        user_1 = User.objects.create_user( "user1", "user@one", "userone")
        user_1.first_name = "UserOne"
        user_1.last_name = "UserOne"
        user_1.save()

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

    #
    # These are our utility methods. It looks like Python doesn't have private methods?
    #

    def assert_off_limits(self, verb, endpoints):
        expected_code = 403
        expected_body = '{"detail": "Authentication credentials were not provided."}'

        for endpoint in endpoints:
            self.request_and_check_response(verb, endpoint, expected_code, expected_body)


    def put_and_check_response(self, path, expected_code, expected_body):
        self.request_and_check_response('put', path, expected_code, expected_body)

    def post_and_check_response(self, path, expected_code, expected_body, **kwargs):
        self.request_and_check_response('post', path, expected_code, expected_body)


    def get_and_check_response(self, path, expected_code, expected_body):
        self.request_and_check_response('get', path, expected_code, expected_body)

    def request_and_check_response(self, verb, path, expected_code, expected_body):
        client = Client()

        response = client.__getattribute__(verb)(path)

        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.content, expected_body)


class AnonymousUserAPIDataTests(AbstractAPIDataTests):
    def test_anonymous_posts_index_get(self):
        """
        Tests that posts index call returns correct values for anonymous user
        """

        expected_body= '[{"id": 3, "published_date": "2012-01-01T17:00:00Z", "user": 2, "title": "PUBLIC Post 2", "body": "This is the post body", "visibility": "PU"}, ' \
                         '{"id": 1, "published_date": "2010-01-01T17:00:00Z", "user": 1, "title": "PUBLIC Post 1", "body": "This is the post body", "visibility": "PU"}]'

        self.get_and_check_response(
            '/api/posts/',
            200,
            expected_body
        )

    def test_anonymous_post_get(self):
        """Tests that post get returns correct value for anonymous user"""
        client = Client()

        self.get_and_check_response(
            '/api/posts/1/',
            200,
            '{"id": 1, "published_date": "2010-01-01T17:00:00Z", "user": 1, "title": "PUBLIC Post 1", "body": "This is the post body", "visibility": "PU"}'
        )

        # This post exists but should not be exposed to anonymous user
        self.get_and_check_response(
            '/api/posts/2/',
            404,
            '{"detail": "Not found"}'
        )


        self.get_and_check_response(
            '/api/posts/3/',
            200,
            '{"id": 3, "published_date": "2012-01-01T17:00:00Z", "user": 2, "title": "PUBLIC Post 2", "body": "This is the post body", "visibility": "PU"}'
        )

        # This post exists but should not be exposed to anonymous user
        self.get_and_check_response(
            '/api/posts/4/',
            404,
            '{"detail": "Not found"}'
        )

        # This post does not exist
        self.get_and_check_response(
            '/api/posts/5/',
            404,
            '{"detail": "Not found"}'
        )

    def test_anonymous_users_get(self):
        expected_body = '[{"id": 1, "username": "user1", "first_name": "UserOne", "last_name": "UserOne", "posts": [2, 1]}, ' \
                        '{"id": 2, "username": "user2", "first_name": "UserTwo", "last_name": "UserTwo", "posts": [4, 3]}]'


        self.get_and_check_response(
            '/api/users/',
            200,
            expected_body
        )

    def test_anonymous_user_get(self):
        self.get_and_check_response(
            '/api/users/1/',
            200,
            '{"id": 1, "username": "user1", "first_name": "UserOne", "last_name": "UserOne", "posts": [2, 1]}'
        )

        self.get_and_check_response(
            '/api/users/2/',
            200,
            '{"id": 2, "username": "user2", "first_name": "UserTwo", "last_name": "UserTwo", "posts": [4, 3]}'
        )

        self.get_and_check_response(
            '/api/users/3/',
            404,
            '{"detail": "Not found"}'
        )

    def test_anonymous_posts(self):
        """Test anonymous posts to all endpoints"""

        endpoints = [
            "/api/users/",
            "/api/posts/",
        ]

        self.assert_off_limits('post', endpoints)



    def test_anonymous_puts(self):
        """Test anonymous puts to all endpoints"""

        endpoints = [
            "/api/users/1/",
            "/api/users/2/",
            "/api/users/3/",
            "/api/posts/1/",
            "/api/posts/2/",
            "/api/posts/3/",
            "/api/posts/4/",
            "/api/posts/5/",
        ]

        self.assert_off_limits('put', endpoints)

    def test_anonymous_deletes(self):
        endpoints = [
            "/api/users/1/",
            "/api/users/2/",
            "/api/users/3/",
            "/api/posts/1/",
            "/api/posts/2/",
            "/api/posts/3/",
            "/api/posts/4/",
            "/api/posts/5/",
        ]

        self.assert_off_limits('delete', endpoints)

class UserActionsIntegrationTests(TestCase):
    def setUp(self):
        User.objects.create_user("testcase", "test@case", "testpass")

    def test_that_good_log_in_succeeds(self):
        client = Client()

        response = client.post('/api/session/', {'username': 'testcase', 'password': 'testpass'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"user_id": 1, "success": true}')

    def test_that_bad_log_in_fails(self):
        client = Client()

        response = client.post('/api/session/', {'username': 'badcase', 'password': 'badpass'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"message": "Invalid username or password", "user_id": null, "success": false}')

class AuthedUserAPIDataTests(AbstractAPIDataTests):
    def test_that_authed_user_can_get_public_post(self):
        expected_code = 200
        expected_body = '{"id": 1, "published_date": "2010-01-01T17:00:00Z", "user": 1, "title": "PUBLIC Post 1", "body": "This is the post body", "visibility": "PU"}'

        self.get_and_check_response('/api/posts/1/', expected_code, expected_body)

    def test_that_authed_user_can_get_draft_post(self):
        expected_code = 200
        expected_body = '{"id": 2, "published_date": "2011-01-01T17:00:00Z", "user": 1, "title": "DRAFT Post 1", "body": "This is the post body", "visibility": "DR"}'

        self.get_and_check_response('/api/posts/2/', expected_code, expected_body)

    def test_that_authed_user_cannot_get_other_user_draft_post(self):
        expected_code = 404
        expected_body = '{"detail": "Not found"}'

        self.get_and_check_response('/api/posts/4/', expected_code, expected_body)

    def test_that_authed_user_can_put_own_post(self):
        expected_code = 200

        # We're changing some data and changing the visibility status
        data = '{"id": 1, "published_date": "2014-04-06T21:50:03Z", "user": 1, "title": "New Document Title", "body": "New Document Body", "visibility": "DR"}'

        self.put_and_check_response('/api/posts/1/', data, expected_code, data)

        # Make sure change took
        expected_body = data

        self.get_and_check_response('/api/posts/1/', expected_code, expected_body)

    def test_that_authed_user_can_post(self):
        expected_code = 201
        expected_body = '{"id": 5, "published_date": "2014-01-01T00:00:00Z", "user": 1, "title": "Test POST", "body": "Please ignore", "visibility": "PU"}'

        data = {
            'published_date': '2014-01-01T00:00:00Z',
            'user': 1,
            'title': 'Test POST',
            'body': 'Please ignore',
            'visibility': 'PU'
        }

        self.post_and_check_response('/api/posts/', data, expected_code, expected_body)

        # Make sure we can GET afterwards

        self.get_and_check_response('/api/posts/5/', 200, expected_body)

    #
    # Redefine utility method for login
    #
    def post_and_check_response(self, path, data, expected_code, expected_body):
        client = Client()

        client.login(username='user1', password='userone')

        response = client.post(path, data)

        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.content, expected_body)

    def put_and_check_response(self, path, data, expected_code, expected_body):
        client = Client()

        client.login(username='user1', password='userone')

        response = client.put(path, data, content_type='application/json')

        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.content, expected_body)

    def request_and_check_response(self, verb, path, expected_code, expected_body, **kwargs):
        client = Client()

        client.login(username='user1', password='userone')

        response = client.__getattribute__(verb)(path, **kwargs)

        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.content, expected_body)