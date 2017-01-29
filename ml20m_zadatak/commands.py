"""
    Paket koji sadrzi glavne funkcije koje se pozivaju za obradu.

    1. download : downloadira arhivirane podatak sa predefinirane (ili defaultne lokacije) lokacije te ih unzipuje
    2. analiza : analizira skup csv-ova po predefiniranim pravilima
    3. svd : vrsi svd analizu po zadanom skupu vektora v sa iteracijama v
    4. preporuke : program predaje listu od movieno preporucenih filmova

"""
import wget
import zipfile
import os
from analiza_filmova import *
from ml_transformacije import *
from dohvat import *

""" Lista konstanti """
const_src = "http://files.grouplens.org/datasets/movielens/ml-20m.zip"
const_dest = "/tmp/"
const_dir_src = "/tmp/ml-20m/"
const_dir_dest = "/tmp/ml-20m/analize/"

def download_unzip(src,dest):
    """
        Funkcija za dohvat podataka sa lokacije te unzip iste
    """
    if src == None:
        src = const_src
    if dest == None:
        dest = const_dest

    wget.download(src,out=dest)
    file_name = src.split("/")[-1]
    with zipfile.ZipFile(dest+file_name,"r") as zip_ref:
        zip_ref.extractall(dest)
    print(" Lokacija i lista csv iz arhive : ")
    for x in zip_ref.namelist():
        print(dest+x)

def analiza(src,dest):
    """
        Funkcija za vrsenje deskriptivnih analiza dataseta m10-20m
    """
    if src == None:
        src = const_dir_src

    if dest==None:
        dest = const_dir_dest
    if not os.path.exists(dest):
        os.makedirs(dest)

    analiza_fimova(src,dest)

def svd_pokretanje(tmp,k):
    """
       Funkcija za SVD obradu i generiranje tablice preporuka
       Funkcija ispisuje MSE algoritma
    """
    if tmp == None:
        tmp = const_dir_src
    if k == None:
        k = 500
    msr = svd_izrada(tmp,k)

    print("Izracunati mean square error : %f" % round(msr,7))

def preporuke(userId,src,n):
    """
      Funkcija za dohvat prvih n
    """
    if src == None:
        src = const_dir_src
    if n == None:
        n = 10

    userId = int(userId)
    dohvat_klijenta(userId,src,n)

if __name__ == '__main__':
    pass
