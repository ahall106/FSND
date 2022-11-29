import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db, setup_db, db_drop_and_create_all, Actor, Movie


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = 'Heyyoo!'
        if excited == 'true':
            greeting = greeting + '! Hi, Hey, Hello; Welcome to the Casting!'
        return greeting

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS'
        )
        return response

    # ROUTES

    '''
        GET /actors
        returns status code 200 and json {"success": True, "actors": actors}
                where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(token):
        actors = Actor.query.all()

        if len(actors) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'actors': [actor.format() for actor in actors],
            }
        )

    '''
        POST /actors
            it should create a new row in the actors table
            it should require the 'post:actors' permission
        returns status code 200 and json {"success": True, "actors": actor}
                where the actor array contains only the newly created actor
            or appropriate status code indicating reason for failure
    '''
    @app.route("/actors", methods=["POST"])
    @requires_auth('post:actors')
    def create_actor(token):
        body = request.json

        if body is None:
            abort(400)

        try:

            actor = Actor(
                name=body.get('name', None),
                age=body.get('age', None),
                gender=body.get('gender', None)
            )
            actor.insert()

        except Exception:
            abort(422)

        return jsonify(
            {
                'success': True,
                'actors': [actor.format()]
            }
        )

    '''
        PATCH /actors/<id>
            where <id> is the existing movie id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:actors' permission
        returns status code 200 and json {"success": True, "actors": actors}
                where the actor array contains only the updated actor
            or appropriate status code indicating reason for failure
    '''
    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth('patch:actors')
    def update_actor(token, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            print(f'Actor with <{id}> not found!')
            abort(404)

        body = request.get_json()

        if body is None:
            abort(400)

        req_name = body.get('name', None)
        req_age = body.get('age', None)
        req_gender = body.get('gender', None)

        try:
            if req_name is not None:
                actor.name = req_name

            if req_age is not None:
                actor.age = req_age

            if req_gender is not None:
                actor.gender = req_gender

            actor.update()

        except Exception:
            abort(422)

        return jsonify(
            {
                'success': True,
                'actors': [actor.format()]
            }
        )

    '''
        DELETE /actors/<id>
            where <id> is the existing actor id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:movies' permission
        returns status code 200 and json {"success": True, "deleted_id": id}
                where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actor(token, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            print(f'Actor with <{id}> not found!')
            abort(404)

        try:
            actor.delete()
        except Exception:
            abort(422)

        return jsonify(
            {
                'success': True,
                'deleted_id': id
            }
        )

    '''
        GET /movies
        returns status code 200 and json {"success": True, "movies": movies}
                where movies is the list of movies
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(token):
        movies = Movie.query.all()

        if len(movies) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'movies': [movie.format() for movie in movies],
            }
        )

    '''
        POST /movies
            it should create a new row in the movies table
            it should require the 'post:movies' permission
        returns status code 200 and json {"success": True, "movies": movie}
                where the movie array contains only the newly created movie
            or appropriate status code indicating reason for failure
    '''
    @app.route("/movies", methods=["POST"])
    @requires_auth('post:movies')
    def create_movie(token):
        body = request.get_json()

        if body is None:
            abort(400)

        try:

            movie = Movie(
                title=body.get('title', None),
                release_date=body.get('release_date', None)
            )
            movie.insert()
        except Exception:
            abort(422)

        return jsonify(
            {
                'success': True,
                'movies': [movie.format()]
            }
        )

    '''
        PATCH /movies/<id>
            where <id> is the existing movie id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:movies' permission
        returns status code 200 and json {"success": True, "movies": movie}
                where the movie array contains only the updated movie
            or appropriate status code indicating reason for failure
    '''
    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth('patch:movies')
    def update_movie(token, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            print(f'Movie with <{id}> not found!')
            abort(404)

        body = request.get_json()

        if body is None:
            abort(400)

        req_title = body.get('title', None)
        req_release_date = body.get('release_date', None)

        try:
            if req_title is not None:
                movie.title = req_title

            if req_release_date is not None:
                movie.release_date = req_release_date

            movie.update()
        except Exception:
            abort(422)

        return jsonify(
            {
                'success': True,
                'movies': [movie.format()]
            }
        )

    '''
        DELETE /movies/<id>
            where <id> is the existing movie id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:movies' permission
        returns status code 200 and json {"success": True, "deleted_id": id}
                where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(token, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            print(f'Movie with <{id}> not found!')
            abort(404)

        try:
            movie.delete()
        except Exception:
            abort(422)

        return jsonify(
            {
                'success': True,
                'deleted_id': id
            }
        )

    # Error Handling

    '''
    implement error handler for 400
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    '''
    implement error handler for 422
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
        }), 422

    '''
    implement error handler for 404
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404

    '''
    implement error handler for AuthError
    '''
    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            'success': False,
            'error': e.status_code,
            'message': e.error['description']
        }), e.status_code

    return app


app = create_app()

'''
Initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
'''
db_drop_and_create_all()

if __name__ == '__main__':
    app.run()
