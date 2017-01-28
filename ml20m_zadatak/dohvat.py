"""
   Funkcije vezane za dohvat klijenta
"""
import pandas as pd

def dohvat_klijenta(user_Id,src,n):
    """
       Funkcija sa lokacije tmp dohvaca df 10M_svd_predikcije koji sadrzi preporucene datasetove
    """
    try:
        movies = pd.read_csv(src+'movies.csv', quotechar='"', skipinitialspace=True)
        ratings_predikcije = pd.read_csv(src+'10M_svd_predikcije.csv', quotechar='"', skipinitialspace=True)
    except FileNotFoundError as e:
        print("Greska u ucitavanju datasetova")

    ratings_p_imena = pd.merge(ratings_predikcije[['movieId','userId','rating']],movies[['movieId','title']])
    lista_preporuka = ratings_p_imena[ratings_p_imena.userId == user_Id].sort_values([('rating')], ascending=False)[:n]
    print(" ")
    print(" Filmske preporuke prvih %s, poredano od najbolje preporuke :",n)
    print("-"*70)
    print(lista_preporuka[['userId','title']])


if __name__ == '__main__':
    pass
