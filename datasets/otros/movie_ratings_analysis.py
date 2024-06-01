from mrjob.job import MRJob
from mrjob.step import MRStep
from statistics import mean

class MovieRatingsAnalysis(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_user_movie_ratings,
                   reducer=self.reducer_user_movie_ratings),
            MRStep(mapper=self.mapper_date_movie_counts,
                   reducer=self.reducer_date_movie_counts),
            MRStep(mapper=self.mapper_movie_user_ratings,
                   reducer=self.reducer_movie_user_ratings),
            MRStep(mapper=self.mapper_date_avg_ratings,
                   reducer=self.reducer_date_avg_ratings),
            MRStep(mapper=self.mapper_genre_movie_ratings,
                   reducer=self.reducer_genre_movie_ratings)
        ]

    # Número de películas vistas por un usuario y valor promedio de calificación
    def mapper_user_movie_ratings(self, _, line):
        try:
            user, movie, rating, genre, date = line.split(',')
            rating = float(rating)
            yield ('user_movie_ratings', user), (movie, rating)
        except:
            pass

    def reducer_user_movie_ratings(self, key, values):
        key_type, user = key
        if key_type == 'user_movie_ratings':
            ratings = list(values)
            num_movies = len(ratings)
            avg_rating = mean(rating for _, rating in ratings)
            yield f'User {user}', {'num_movies': num_movies, 'avg_rating': avg_rating}

    # Día en que más y menos películas se han visto
    def mapper_date_movie_counts(self, _, line):
        try:
            user, movie, rating, genre, date = line.split(',')
            yield ('date_movie_counts', date), 1
        except:
            pass

    def reducer_date_movie_counts(self, key, values):
        key_type, date = key
        if key_type == 'date_movie_counts':
            total_movies = sum(values)
            yield f'Date {date}', {'total_movies': total_movies}

    # Número de usuarios que ven una misma película y el rating promedio
    def mapper_movie_user_ratings(self, _, line):
        try:
            user, movie, rating, genre, date = line.split(',')
            rating = float(rating)
            yield ('movie_user_ratings', movie), (user, rating)
        except:
            pass

    def reducer_movie_user_ratings(self, key, values):
        key_type, movie = key
        if key_type == 'movie_user_ratings':
            ratings = list(values)
            num_users = len(ratings)
            avg_rating = mean(rating for _, rating in ratings)
            yield f'Movie {movie}', {'num_users': num_users, 'avg_rating': avg_rating}

    # Día en que peor y mejor evaluación en promedio han dado los usuarios
    def mapper_date_avg_ratings(self, _, line):
        try:
            user, movie, rating, genre, date = line.split(',')
            rating = float(rating)
            yield ('date_avg_ratings', date), rating
        except:
            pass

    def reducer_date_avg_ratings(self, key, values):
        key_type, date = key
        if key_type == 'date_avg_ratings':
            ratings = list(values)
            avg_rating = mean(ratings)
            yield f'Date {date}', {'avg_rating': avg_rating}

    # La mejor y peor película evaluada por género
    def mapper_genre_movie_ratings(self, _, line):
        try:
            user, movie, rating, genre, date = line.split(',')
            rating = float(rating)
            yield ('genre_movie_ratings', (genre, movie)), rating
        except:
            pass

    def reducer_genre_movie_ratings(self, key, values):
        key_type, (genre, movie) = key
        if key_type == 'genre_movie_ratings':
            ratings = list(values)
            avg_rating = mean(ratings)
            yield f'Genre {genre}, Movie {movie}', {'avg_rating': avg_rating}

if __name__ == '__main__':
    MovieRatingsAnalysis.run()
