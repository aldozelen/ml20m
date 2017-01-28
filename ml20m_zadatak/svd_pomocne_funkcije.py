"""
    Pomocne funkcije za SVD methodu
"""

import pickle
import pandas as pd
import numpy as np


def svd_izgradnja_liste(tmp,train_mat,user_indices,users,movies):
    """
       Funkcija za izgradnju pandas df iz SVD prediktivne matrice
       te spremanje istog
    """

    ratings_predicted = pd.DataFrame([],columns=['userId', 'movieId','rating'])
    with open(tmp+'10M_svd_predikcije.csv', 'w') as f:
        ratings_predicted.to_csv(f)

    for user_id in users:

        lista = train_mat[user_indices[user_id]][:].toarray()[0]
        vektor = np.in1d(lista,0,invert=True)

        data = {'userId':[user_id]*len(movies[vektor]),
           'movieId':movies[vektor],
           'rating':X_lr[user_indices[user_id]][vektor]      }

        df_tmp = pd.DataFrame(data, columns=['userId', 'movieId','rating'])
        with open(tmp+'10M_svd_predikcije.csv', 'a') as f:
            df_tmp.to_csv(f, header=False)


if __name__ == "__main__":
    pass
