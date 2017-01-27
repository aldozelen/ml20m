"""Calculator using docopt

Usage:
  ml20m_zadatak.py download [--izvor=src] [--odrediste=desc]
  ml20m_zadatak.py analiza [--odrediste=desc]
  ml20m_zadatak.py svd [--tmp = desc] [--vektori = v] [--iter = k]
  ml20m_zadatak.py preporuke --userid=user [--br_filmova=movieno]
  ml20m_zadatak.py (-h | --help)

Arguments
  download Math Operation
  analiza Analiza dataset-a
  svd SVD Fakorizacija dataset-a
  preporuke Izlist preporuka za user-a
  --userid = user Id usera, korisnika, za kojeg trazimo filmske preporuke

Options:
  -h --help     Show this screen
  --izvor = src Izvor za download CSV
  --odrediste = desc Lokalna lokacija za spremanje CSV-a3
  --vektori = v Broj vektora
  --br_filmova = Broj filmova  movieno
  --iter = k broj iteracija
  --tmp = desc Direktorij za spremanje tmp filova cc 15 GB

"""
from docopt import docopt
import commands as cm

if __name__ == '__main__':
    try:
    # Parse arguments, use file docstring as a parameter definition
        arguments = docopt(__doc__, version='Calculator with docopt')

        if arguments['download'] :
            cm.download_unzip(arguments["--izvor"],arguments["--odrediste"])
        elif arguments['analiza'] :
            cm.analiza(arguments["--odrediste"])
        elif arguments['svd'] :
            print('svd')
        elif arguments['preporuke'] :
            print('preporuke')

    # Handle invalid options
    except docopt.DocoptExit as e:
        print e.message