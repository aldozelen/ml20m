import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def analiza_fimova(src,dest):
    """
        Fiksne analize i izlaz za obradu filmova :
        1. Barchart plot frekvencija po zarnovima
        2. Barchart plot po godinama, mjesecima i satima u danu
        3. Lista 20 najgledanijih filmova (tj. najcesce ocjenjenih filmova)
        4. Lista 20 najbolje ocijenjenih filmova sa barem 100 ocjena
        5. Lista 20 najkontroverznijih filmova sa barem 1000 ocjena
    """

    try:
        movies = pd.read_csv(src+'movies.csv', quotechar='"', skipinitialspace=True)
        ratings = pd.read_csv(src+'ratings.csv', quotechar='"', skipinitialspace=True)
    except FileNotFoundError as e:
        print("Greska u ucitavanju datasetova")

    s = movies['genres'].str.split('|').apply(pd.Series,1).stack()
    s.index = s.index.droplevel(-1) # to line up with movie's index
    s.name = 'genres'

    s = movies['genres'].str.split('|').apply(pd.Series,1).stack()
    s.index = s.index.droplevel(-1) # to line up with movie's index
    s.name = 'genres'

    del movies['genres']
    movies_genres = movies.join(s)

    # Bar chart koji prikazuje popularnost zarnova
    fig, ax = plt.subplots()
    movies_genres['genres'].value_counts().plot(ax=ax, kind='bar')
    plt.tight_layout()
    fig.savefig(dest+'frekvencije_po_zanrovima.png')

    del movies_genres

    # Dodavanje vremenske dimenzije iz unix timestampa
    ratings['timestamp'] = pd.to_datetime(ratings['timestamp'],unit='s')
    ratings['year'] = pd.DatetimeIndex(ratings['timestamp']).year
    ratings['month'] = pd.DatetimeIndex(ratings['timestamp']).month
    ratings['hour'] = pd.DatetimeIndex(ratings['timestamp']).hour

    # Ocjene po godinama
    fig, ax = plt.subplots()
    ratings['year'].value_counts(sort = False).plot(ax=ax, kind='bar')
    plt.tight_layout()
    fig.savefig(dest+'ocjene_po_godinama.png')

    # Ocjene po mjesecima
    fig, ax = plt.subplots()
    ratings['month'].value_counts(sort = False).plot(ax=ax, kind='bar')
    plt.tight_layout()
    fig.savefig(dest+'ocjene_po_mjesecima.png')

    # Ocjene po satima
    fig, ax = plt.subplots()
    ratings['hour'].value_counts(sort = False).plot(ax=ax, kind='bar')
    plt.tight_layout()
    fig.savefig(dest+'ocjene_po_satima.png')

    # Rating i informacije o filmovima skupa
    movie_ratings = pd.merge(movies, ratings[['movieId','rating']])

    # Statistike nad ratinzima filmovima
    movie_stats = movie_ratings.groupby('title').agg({'rating': [np.size, np.mean,np.median,np.std]})

    # Filmovi koji imaju barem 100 ocjena
    atleast_100 = movie_stats['rating']['size'] >= 100

    # Filmovi koji imaju barem 1000 ocjena
    atleast_1000 = movie_stats['rating']['size'] >= 1000

    # 20 najocjenivanijih ffilmova
    tmp_out = movie_stats.sort_values([('rating', 'size')], ascending=False)[:20]
    tmp_out.to_csv(dest+"20_najgledanih.csv", sep=',', encoding='utf-8')

    # 20 najbolje ocijenjenih filmova koji imaju barem 100 ocjena
    tmp_out = movie_stats[atleast_100].sort_values([('rating', 'mean')], ascending=False)[:20]
    tmp_out.to_csv(dest+"20_najboljih_m20.csv", sep=',', encoding='utf-8')

    # 20 najkontroverznijih filmova koji imaju barem 1000 ocjena
    tmp_out = movie_stats[atleast_1000].sort_values([('rating', 'std')], ascending=False)[:20]
    tmp_out.to_csv(dest+"20_najkontroverznijih_m20.csv", sep=',', encoding='utf-8')

if __name__ == '__main__':
    pass
