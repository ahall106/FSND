import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from settings import CASTING_ASSISTANT_TOKEN, CASTING_DIRECTOR_TOKEN,\
    EXECUTIVE_PRODUCER_TOKEN


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.casting_assistant_auth = f'Bearer {CASTING_ASSISTANT_TOKEN}'
        self.casting_director_auth = f'Bearer {CASTING_DIRECTOR_TOKEN}'
        self.executive_producer_auth = f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'

        self.new_actor = {
            "name": "Kitty Hall",
            "age": 55,
            "gender": "Male",
        }

        self.actor_with_age_change = {
            "age": 22,
        }

        self.new_movie = {
            "title": "",
            "release_date": "01/06/2023"
        }

        self.movie_with_release_date = {
            "release_date": "07/27/2027"
        }

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    '''
    RBAC TEST
    '''

    def test_get_movies_by_casting_assistant_with_auth_200(self):
        response = self.client().get(
            '/movies',
            headers={'Authorization': self.casting_assistant_auth})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_by_casting_assistant_with_auth_200(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': self.casting_assistant_auth})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_by_casting_assistant_without_auth_401(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    def test_get_actors_by_casting_assistant_without_auth_401(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    def test_post_movies_by_casting_assistant_without_auth_403(self):
        response = self.client().post(
            '/movies',
            headers={'Authorization': self.casting_assistant_auth},
            json=self.new_movie
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)

    def test_post_actors_by_casting_assistant_without_auth_403(self):
        response = self.client().post(
            '/actors',
            headers={'Authorization': self.casting_assistant_auth},
            json=self.new_actor
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)

    def test_patch_movies_by_casting_assistant_without_auth_403(self):
        response = self.client().patch(
            '/movies/1',
            headers={'Authorization': self.casting_assistant_auth},
            json=self.movie_with_release_date
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)

    def test_patch_actors_by_casting_assistant_without_auth_403(self):
        response = self.client().patch(
            '/actors/2',
            headers={'Authorization': self.casting_assistant_auth},
            json=self.actor_with_age_change
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)

    def test_delete_movies_by_casting_assistant_without_auth_403(self):
        response = self.client().delete(
            'movies/1',
            headers={'Authorization': self.casting_assistant_auth}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)

    def test_delete_actors_by_casting_assistant_without_auth_403(self):
        response = self.client().delete(
            'actors/2',
            headers={'Authorization': self.casting_assistant_auth}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)

    def test_post_actors_by_casting_director_with_auth_200(self):
        response = self.client().post(
            '/actors',
            headers={'Authorization': self.casting_director_auth},
            json=self.new_actor
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_post_movies_by_executive_producer_with_auth_200(self):
        response = self.client().post(
            '/movies',
            headers={'Authorization': self.executive_producer_auth},
            json=self.new_movie
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_patch_movies_by_casting_director_with_auth_200(self):
        response = self.client().patch(
            '/movies/2',
            headers={'Authorization': self.casting_director_auth},
            json=self.movie_with_release_date
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_patch_actors_by_casting_director_with_auth_200(self):
        response = self.client().patch(
            '/actors/1',
            headers={'Authorization': self.casting_director_auth},
            json=self.actor_with_age_change
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_delete_movies_by_executive_producer_with_auth_200(self):
        response = self.client().delete(
            'movies/1',
            headers={'Authorization': self.executive_producer_auth}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 1)

    def test_delete_actors_by_executive_producer_with_auth_200(self):
        response = self.client().delete(
            'actors/2',
            headers={'Authorization': self.executive_producer_auth}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 2)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
