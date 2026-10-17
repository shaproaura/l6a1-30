import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

ratings_df = pd.read_csv('ratings.csv')
ratings_df.head()

movies_df = pd.read_csv('movies.csv')
movies_df.head()

movies_df['year'] = movies_df.title.str.extract(r'(\(\d\d\d\d\))', expand=True)
movies_df['year'] = movies_df.year.str.extract(r'(\d\d\d\d)', expand=True)

movies_df['title'] = movies_df.title.str.replace(r'(\(\d\d\d\d\))', '', regex=True)
movies_df['title'] = movies_df['title'].apply(lambda x: x.strip())

movies_df.head()

movies_df['genres'] = movies_df.genres.str.split('|')

movies_copy = movies_df.copy()
for index, row in movies_df.iterrows():
    for genre in row['genres']:
        movies_copy.at[index, genre] = 1

movies_copy = movies_copy.fillna(0)
movies_copy.head()

ratings_df = ratings_df.drop(['timestamp'], axis=1)
ratings_df.head()

genre_columns = movies_copy.drop(['movieId', 'title', 'genres', 'year'], axis=1)
genre_counts = genre_columns.sum().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
plt.bar(genre_counts.index, genre_counts.values, color='#4C9AFF')
plt.title('Movies Per Genre')
plt.xlabel('Genre')
plt.ylabel('Number of Movies')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()



user_input = [
    {'title': 'Grand Slam', 'rating': 5.6},
    {'title': 'Zero', 'rating': 7},
    {'title': 'Toy Story', 'rating': 4.5}
]

movie_input = pd.DataFrame(user_input)
movie_input

input_id = movies_df[movies_df['title'].isin(movie_input['title'].tolist())]
movie_input = pd.merge(input_id, movie_input)
movie_input = movie_input.drop(['genres', 'year'], axis=1)
movie_input

movie_user = movies_copy[movies_copy['movieId'].isin(movie_input['movieId'].tolist())]
movie_user = movie_user.reset_index(drop=True)

UserGenreTable =movie_user.drop(['movieId', 'title', 'genres', 'year'], axis=1)

Userprofile = UserGenreTable.transpose().dot(movie_input['rating'])

plt.figure(figsize=(10, 5))
plt.bar(Userprofile.index, Userprofile.values, color='#FF6B6B')
plt.title('Your Taste Profile')
plt.xlabel('Genre')
plt.ylabel('Weight')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

GenreTable = movies_copy.se_index(movies_copy['movieId'])
GenreTable = GenreTable.drop(['movieId', 'title', 'genres', 'year'], axis=1)

Recommendation_df = ((GenreTable * Userprofile).sum(axis=1)) / Userprofile.sum()
Recommendation_df = Recommendation_df.sort_values(ascending=False)
Recommendation_df.head()

Recommendation_Tabel = movies_df.loc[movies_df['movieId'].isin(Recommendation_df.head(20).keys())]

top10_score = Recommendation_df.head(10)
top12_title = movies_df.set_index('movieId').loc[top10_score.index]['title']

plt.figure(figsize=(8, 6))
plt.brah(top12_title[::-1], top10_score.values[::-1],color='#51CF66')
plt.title("Top 10 Picks")
plt.xlabel('March Score')
plt.tight_layout()
plt.show()
