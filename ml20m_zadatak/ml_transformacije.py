"""
    Paket sa ml algoritmima
    1. svd_izrada : Singular value decomposition analiza
"""

import pandas as pd
import numpy as np
import scipy.sparse as sp
import os.path as path
import pickle

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
    try:
        ratings = pd.read_csv(tmp+'ratings.csv', quotechar='"', skipinitialspace=True)
    except FileNotFoundError as e:
        print("Greska u ucitavanju datasetova")

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

    """" Fiksno pozivamo 10 filmova po korisniku za testni skup"""
    train, test = train_test_split_df(ratings)

    """" Sparse matrica za spremanje rezultata """"
    train_mat = sp.lil_matrix((number_of_rows, number_of_columns))
    #test_mat  = sp.lil_matrix((number_of_rows, number_of_columns))

    """ Dodavanje podatak u train matricu"""
    for line in train.values:
        u, i , r , gona = map(int,line)
        train_mat[user_indices[u], movie_indices[i]] = r

    """" Dodavanje podatak u test matricu""""
    """for line in test.values:
        u, i , r , gona = map(int,line)
        test_mat[user_indices[u], movie_indices[i]] = r"""

    """" Ucitavanje stvorenih matrixa """"
    if os.path.isfile(tmp+"10M_svd_u.pickle") & os.path.isfile(tmp+"10M_svd_s.pickle") & os.path.isfile(tmp+"10M_svd_vt.pickle"):
        u = pickle.load( open( tmp+"10M_svd_u.pickle", "rb" ) )
        s = pickle.load( open( tmp+"10M_svd_s.pickle", "rb" ) )
        vt = pickle.load( open( tmp+"10M_svd_vt.pickle", "rb" ) )
    else :
        u, s, vt = svds(train_mat, k )

    s_diag_matrix = np.zeros((s.shape[0], s.shape[0]))

    for i in range(s.shape[0]):
        s_diag_matrix[i,i] = s[i]

    inter_matrix = np.dot(u, s_diag_matrix)

    """ Stvaranje memmapa zbog velicine matrice cc 15 GB """
    filename = path.join(mkdtemp(), 'newfile.dat')
    X_lr = np.memmap(filename,dtype='float32',mode='w+',shape=(inter_matrix.shape[0],vt.shape[1]))

    """ Kreiranje matrice preporuka """
    X_lr = chunking_dot(inter_matrix, vt)

    """ Kreiranje testne matrice """
    filename = path.join(mkdtemp(), 'testfile.dat')
    Y_lr = np.memmap(filename,dtype='float32',mode='w+',shape=(len(user_indices),len(movie_indices)))

    for line in test.values:
        u, i , r , gona = map(int,line)
        Y_lr[user_indices[u], movie_indices[i]] = r

    svd_izgradnja_liste(tmp,train_mat,user_indices,users,movies)

    return mse(X_lr,Y_lr)

if __name__ == '__main__':
    pass
