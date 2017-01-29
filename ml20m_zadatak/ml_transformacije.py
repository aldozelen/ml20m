"""
    Paket sa ml algoritmima
    1. svd_izrada : Singular value decomposition analiza
"""

import pandas as pd
import os
import numpy as np
import scipy.sparse as sp
import os.path as path
import pickle
import time

from scipy.sparse.linalg import svds
from tempfile import mkdtemp
from pomocne_funkcije import *
from svd_pomocne_funkcije import *


def svd_izrada(tmp,k):
    """
        Funkcija za izradu matrice preporuke po SVD algoritmu
        Rezlutati se zapisuju kao pandas dataset pickle methodom
        Funkcija fiksno prihvaca ratings tablicu i po njoj racuna novu tablicu preporuka
    """
    t0 = time.time()
    try:
        ratings = pd.read_csv(tmp+'ratings.csv', quotechar='"', skipinitialspace=True)
    except FileNotFoundError as e:
        print("Greska u ucitavanju datasetova")
    t1 = time.time()

    print("Ucitani podaci iz csv-a u trajanju %i s " % (t1-t0))

    t0 = time.time()
    users = np.unique(ratings['userId'])
    movies = np.unique(ratings['movieId'])

    number_of_rows = len(users)
    number_of_columns = len(movies)

    """ Kreiramo dictionary id-a filma/user-a i slijednog broja"""
    movie_indices, user_indices = {}, {}

    for i in range(len(movies)):
        movie_indices[movies[i]] = i

    for i in range(len(users)):
        user_indices[users[i]] = i

    """ Fiksno pozivamo 10 filmova po korisniku za testni skup """
    train, test = train_test_split_df(ratings)

    """" Sparse matrica za spremanje rezultata """
    train_matrica = sp.lil_matrix((number_of_rows, number_of_columns))

    """ Dodavanje podatak u train matricu """
    for line in train.values:
        u, i , r , gona = map(int,line)
        train_matrica[user_indices[u], movie_indices[i]] = r
    t1 = time.time()

    print("Ucitana training matrica u trajanju %i s " % (t1-t0))
    t0 = time.time()

    """ Ucitavanje prije stvorenih matrixa """
    if path.isfile(tmp+"10M_svd_u.pickle") & path.isfile(tmp+"10M_svd_s.pickle") & path.isfile(tmp+"10M_svd_vt.pickle"):
        u = pickle.load( open( tmp+"10M_svd_u.pickle", "rb" ) )
        s = pickle.load( open( tmp+"10M_svd_s.pickle", "rb" ) )
        vt = pickle.load( open( tmp+"10M_svd_vt.pickle", "rb" ) )
    else :
        t01 = time.time()
        u, s, vt = svds(train_matrica, k )

        with open(tmp+"10M_svd_u.pickle", 'wb') as handle:
            pickle.dump(u, handle)
        with open(tmp+"10M_svd_s.pickle", 'wb') as handle:
            pickle.dump(s, handle)
        with open(tmp+"10M_svd_vt.pickle", 'wb') as handle:
            pickle.dump(vt, handle)

        t11 = time.time()
        print("Izvrsen SVD algoritam u trajanju %s s ",t11-t01)

    s_diag_matrix = np.zeros((s.shape[0], s.shape[0]))

    for i in range(s.shape[0]):
        s_diag_matrix[i,i] = s[i]

    inter_matrix = np.dot(u, s_diag_matrix)

    """ Stvaranje memmapa zbog velicine matrice cc 15 GB """
    filename = path.join(mkdtemp(), 'newfile.dat')
    X_lr = np.memmap(filename,dtype='float32',mode='w+',shape=(inter_matrix.shape[0],vt.shape[1]))

    """ Kreiranje matrice preporuka """
    chunking_dot(X_lr,inter_matrix, vt)

    t1 = time.time()
    print("Kreirana matrica preporuka  %i s " % (t1-t0))
    t0 = time.time()

    """ Kreiranje testne matrice cc 15 GB"""
    filename_test = path.join(mkdtemp(), 'testfile.dat')
    Y_lr = np.memmap(filename_test,dtype='float32',mode='w+',shape=(len(user_indices),len(movie_indices)))

    for line in test.values:
        u, i , r , gona = map(int,line)
        Y_lr[user_indices[u], movie_indices[i]] = r

    t1 = time.time()
    print("Kreiranje testne matrice %i s " % (t1-t0))

    t0 = time.time()
    svd_izgradnja_liste(tmp,X_lr,train_matrica,user_indices,users,movies)
    t1 = time.time()

    print("Dataset za preporuke generiran %i s " % (t1-t0))
    mean_sqr_error = mse(X_lr,Y_lr)

    X_lr._mmap.close()
    Y_lr._mmap.close()

    return mean_sqr_error

if __name__ == '__main__':
    pass
