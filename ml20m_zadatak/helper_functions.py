import pandas as pd
import os.path as path
import numpy as np
from tempfile import mkdtemp

def train_test_split_df(df,num_row = 10,column ='userId'):
    """
        Funkcija za razlamanje ulaznog pandas dataframe-a na testni i
        training skup
    """
    def ranker(df,seed = 0, sample_size = 10):
        """
            Funkcija za označavanje  sample_size odabranih brojeva
        """
        np.random.seed(0)
        arr = np.array([1] * sample_size + [0] * (len(df)-sample_size))
        np.random.shuffle(arr)
        df['choice'] = arr
        return df
    localDf = pd.DataFrame(df[column])
    localDf = localDf.groupby(column).apply(ranker)
    train = df[localDf['choice']==0]
    test = df[localDf['choice']==1]
    return train, test

def chunking_dot(big_matrix, small_matrix, chunk_size=1000):
    """
        Funkcija za sporiji memorijski sigurniji DOT produkt
    """
    filename = path.join(mkdtemp(), 'newfile.dat')
    R = np.memmap(filename,dtype='float32',mode='w+',shape=(big_matrix.shape[0],small_matrix.shape[1]))
    for i in range(0, R.shape[0], chunk_size):
        end = i + chunk_size
        R[i:end] = np.dot(big_matrix[i:end], small_matrix)
    return R

def mse(X_lr,Y_lr):
    """
        Algoritam za iterativno računanje mean square error-a
    """
    suma = 0
    for i in range(X_lr.shape[0]):
        suma = suma + np.square(X_lr[i][:]-Y_lr[i][:]).sum()
    return suma/(X_lr.shape[0]*X_lr.shape[1])

if __name__ == "__main__":
    pass
