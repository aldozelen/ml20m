import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def analiza_fimova(src,dest):
    """
        Fiksne analize i izlaz za obradu filmova
    """

    try:
        movies = pd.read_csv(src+'movies.csv', quotechar='"', skipinitialspace=True)
        ratings = pd.read_csv(src+'ratings.csv', quotechar='"', skipinitialspace=True)
        links = pd.read_csv(src+'links.csv', quotechar='"', skipinitialspace=True)
        tags = pd.read_csv(src+'tags.csv', quotechar='"', skipinitialspace=True)
        genome_scores = pd.read_csv(src+'genome-scores.csv', quotechar='"', skipinitialspace=True)
        genome_tags = pd.read_csv(src+'genome-tags.csv', quotechar='"', skipinitialspace=True)
    except e:
        print("Greska u ucitavanju datasetova")

    s = movies['genres'].str.split('|').apply(pd.Series,1).stack()
    s.index = s.index.droplevel(-1) # to line up with movie's index
    s.name = 'genres'

    s = movies['genres'].str.split('|').apply(pd.Series,1).stack()
    s.index = s.index.droplevel(-1) # to line up with movie's index
    s.name = 'genres'

    del movies['genres']
    movies = movies.join(s)

    fig, ax = plt.subplots()
    movies['genres'].value_counts().plot(ax=ax, kind='bar')
    plt.tight_layout()
    fig.savefig('frekvencije.png')

    ratings['timestamp'] = pd.to_datetime(ratings['timestamp'],unit='s')
    ratings['year'] = pd.DatetimeIndex(ratings['timestamp']).year
    ratings['month'] = pd.DatetimeIndex(ratings['timestamp']).month
    ratings['hour'] = pd.DatetimeIndex(ratings['timestamp']).hour

    #Ocjene po godinama
    fig, ax = plt.subplots()
    ratings['year'].value_counts(sort = False).plot(ax=ax, kind='bar')
    plt.tight_layout()
    fig.savefig('ocjene_po_godinama.png')

    #Ocjene po mjesecima
    fig, ax = plt.subplots()
    ratings['month'].value_counts(sort = False).plot(ax=ax, kind='bar')
    plt.tight_layout()
    fig.savefig('ocjene_po_mjesecima.png')

    #Ocjene po satima
    fig, ax = plt.subplots()
    ratings['hour'].value_counts(sort = False).plot(ax=ax, kind='bar')
    plt.tight_layout()
    fig.savefig('ocjene_po_satima.png')

    #Ratinzi
    movie_ratings = pd.merge(movies, ratings[['movieId','rating']])

    s = movie_ratings['genres'].str.split('|').apply(pd.Series,1).stack()
    s.index = s.index.droplevel(-1) # to line up with movie's index
    s.name = 'genres'

    del movie_ratings['genres']
    movie_ratings = movie_ratings.join(s)

    atleast_100 = movie_stats['rating']['size'] >= 100

    tmp_out = movie_stats[atleast_100].sort_values([('rating', 'mean')], ascending=False)[:15]
    tmp_out.to_csv("atleast100_sorted.csv", sep='\t', encoding='utf-8')

    # Koji su najgledanijj najbolje ocijenivani filmovi
    tmp_out = movie_stats.sort_values([('rating', 'size')], ascending=False).sort_values([('rating', 'size')], ascending=False).head()
    tmp_out.to_csv(("najgledaniji.csv", sep='\t', encoding='utf-8')

    # Standard deviation of rating grouped by title
    rating_std_by_title = ratings.groupby('movieId')['rating'].std()
    # Filter down to active_titles
    rating_std_by_title = rating_std_by_title.ix[atleast_100]
    # Order Series by value in descending order
    tmp_out = rating_std_by_title.order(ascending=False)[:10]
    tmp_out.to_csv(("kontroverzni.csv", sep='\t', encoding='utf-8')

if __name__ == '__main__':
    pass
