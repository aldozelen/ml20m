"""
    Paket koji sadrzi glavne funkcije koje se pozivaju za obradu.

    1. download : downloadira arhivirane podatak sa predefinirane (ili defaultne lokacije) lokacije te ih unzipuje
    2. analiza : analizira skup csv-ova po predefiniranim pravilima
    3. svd : vrsi svd analizu po zadanom skupu vektora v sa iteracijama v
    4. preporuke : program predaje listu od movieno preporucenih filmova

"""
import urllib
import wget
import zipfile

const_src = "http://files.grouplens.org/datasets/movielens/ml-20m.zip"
const_dest = "/tmp/"

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

def analiza(dest):
    """
        Funkcija za vrsenje deskriptivnih analiza dataseta m10-20m
    """

if __name__ == '__main__':
    pass
