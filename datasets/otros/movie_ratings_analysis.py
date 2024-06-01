from mrjob.job import MRJob
from mrjob.step import MRStep
from statistics import mean

class MovieRatingsAnalysis(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_user_ratings,
                   reducer=self.reducer_user_ratings),
            MRStep(mapper=self.mapper_date_movies,
                   reducer=self.reducer_date_movies),
            MRStep(mapper=self.mapper_movie_ratings,
                   reducer=self.reducer_movie_ratings),
            MRStep(mapper=self.mapper_date_avg_rating,
                   reducer=self.reducer_date_avg_rating),
            MRStep(mapper=self.mapper_genre_ratings,
                   reducer=self.reducer_genre_ratings)
        ]

    def mapper_user_ratings(self, _, line):
        try:
            fields = line.split(',')
            if len(fields) == 5:
                user, movie, rating, genre, date = fields
                rating = float(rating)
                yield ('user_ratings', user), (movie, rating)
                yield ('date_movies', date), 1
                yield ('movie_ratings', movie), (user, rating)
                yield ('date_avg_rating', date), rating
                yield ('genre_ratings', (genre, movie)), rating
        except Exception as e:
            self.increment_counter('errors', 'bad_lines', 1)
            self.log(f"Error processing line: {line}\n{str(e)}")

    def reducer_user_ratings(self, key, values):
        key_type, key_val = key
        if key_type == 'user_ratings':
            movies = list(values)
            num_movies = len(movies)
            avg_rating = mean(rating for _, rating in movies)
            yield f'User {key_val}', {'num_movies': num_movies, 'avg_rating': avg_rating}
        elif key_type == 'date_movies':
            total_movies = sum(values)
            yield f'Date {key_val}', {'total_movies': total_movies}
        elif key_type == 'movie_ratings':
            users = list(values)
            num_users = len(users)
            avg_rating = mean(rating for _, rating in users)
            yield f'Movie {key_val}', {'num_users': num_users, 'avg_rating': avg_rating}
        elif key_type == 'date_avg_rating':
            ratings = list(values)
            avg_rating = mean(ratings)
            yield f'Date {key_val}', {'avg_rating': avg_rating}
        elif key_type == 'genre_ratings':
            ratings = list(values)
            avg_rating = mean(ratings)
            genre, movie = key_val
            yield f'Genre {genre}, Movie {movie}', {'avg_rating': avg_rating}

    def mapper_date_movies(self, key, value):
        if key.startswith('Date'):
            yield key, value['total_movies']

    def reducer_date_movies(self, key, values):
        values_list = list(values)
        if key.startswith('Date'):
            if 'most_movies_date' not in self.options:
                self.options.most_movies_date = (key, max(values_list))
                self.options.least_movies_date = (key, min(values_list))
            else:
                if max(values_list) > self.options.most_movies_date[1]:
                    self.options.most_movies_date = (key, max(values_list))
                if min(values_list) < self.options.least_movies_date[1]:
                    self.options.least_movies_date = (key, min(values_list))

            yield self.options.most_movies_date[0], 'Most movies seen'
            yield self.options.least_movies_date[0], 'Least movies seen'

    def mapper_movie_ratings(self, key, value):
        if key.startswith('Movie'):
            yield key, value

    def reducer_movie_ratings(self, key, values):
        yield key, list(values)

    def mapper_date_avg_rating(self, key, value):
        if key.startswith('Date'):
            yield key, value['avg_rating']

    def reducer_date_avg_rating(self, key, values):
        values_list = list(values)
        avg_rating = mean(values_list)
        yield key, avg_rating

        if 'best_avg_rating_date' not in self.options:
            self.options.best_avg_rating_date = (key, avg_rating)
            self.options.worst_avg_rating_date = (key, avg_rating)
        else:
            if avg_rating > self.options.best_avg_rating_date[1]:
                self.options.best_avg_rating_date = (key, avg_rating)
            if avg_rating < self.options.worst_avg_rating_date[1]:
                self.options.worst_avg_rating_date = (key, avg_rating)

        yield self.options.best_avg_rating_date[0], 'Best average rating'
        yield self.options.worst_avg_rating_date[0], 'Worst average rating'

    def mapper_genre_ratings(self, key, value):
        if key.startswith('Genre'):
            yield key, value['avg_rating']

    def reducer_genre_ratings(self, key, values):
        avg_rating = mean(list(values))
        yield key, avg_rating

if __name__ == '__main__':
    MovieRatingsAnalysis.run()
