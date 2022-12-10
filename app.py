from flask import Flask, request
from flask_restx import Api, Resource

from models import Movie, Genre, Director
from schemas import movie_schema, movies_schema, directors_schema, director_schema, genres_schema, genre_schema
from setup_db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JSON_AS_ASCII'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Связываем контекст с приложением
app.app_context().push()
# Связываем базу данных и приложение
db.init_app(app)

api = Api(app)
movie_ns = api.namespace("movies")
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")


@movie_ns.route("/")
class MoviesView(Resource):

    def get(self):
        movies = db.session.query(Movie)

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        if director_id:
            movies = movies.filter(Movie.director_id == director_id)
        if genre_id:
            movies = movies.filter(Movie.genre_id == genre_id)

        all_movies = movies.all()
        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return f"Новый объект с id{db.session.id} создан", 201


@movie_ns.route("/<int:movie_id>")
class MovieView(Resource):

    def get(self, movie_id: int):
        movie = db.session.query(Movie).get(movie_id)
        if movie:
            return movie_schema.dump(movie), 200
        return 404

    def put(self, movie_id: int):
        movie = db.session.query(Movie).get(movie_id)
        if movie:
            req_json = request.json

            movie.title = req_json['title']
            movie.description = req_json['description']
            movie.trailer = req_json['trailer']
            movie.year = req_json['year']
            movie.rating = req_json['rating']
            movie.genre_id = req_json['genre_id']
            movie.director_id = req_json['director_id']
            db.session.add(movie)
            db.session.commit()
            return f"Фильм с id{movie_id} обнавлён.", 204
        return f"Фильм не найден", 404


@director_ns.route("/")
class DirectorsView(Resource):

    def get(self):
        directors = db.session.query(Director)

        all_directors = directors.all()
        return directors_schema.dump(all_directors), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return f"Новый объект с id{db.session.id} создан", 201


@director_ns.route("/<int:director_id>")
class DirectorView(Resource):

    def get(self, director_id: int):
        director = db.session.query(Director).get(director_id)
        if director:
            return director_schema.dump(director), 200
        return 404

    def put(self, director_id: int):
        director = db.session.query(Director).get(director_id)
        if director:
            req_json = request.json

            director.name = req_json['name']

            db.session.add(director)
            db.session.commit()
            return f"Режессёр с id{director_id} обнавлён.", 204
        return f"Режессёр не найден", 404


@genre_ns.route("/")
class GenresView(Resource):

    def get(self):
        genres = db.session.query(Genre)

        all_genres = genres.all()
        return genres_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        all_genres = Genre(**req_json)
        with db.session.begin():
            db.session.add(all_genres)
        return f"Новый объект с id{db.session.id} создан", 201


@genre_ns.route("/<int:genre_id>")
class GenresView(Resource):

    def get(self, genre_id: int):
        genre = db.session.query(Genre).get(genre_id)
        if genre:
            return genre_schema.dump(genre), 200
        return 404

    def put(self, genre_id: int):
        genre = db.session.query(Genre).get(genre_id)
        if genre:
            req_json = request.json

            genre.name = req_json['name']

            db.session.add(genre)
            db.session.commit()
            return f"Жанр с id{genre_id} обнавлён.", 204
        return f"Жанр не найден", 404


if __name__ == '__main__':
    app.run(debug=True)
