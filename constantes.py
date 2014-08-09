#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import requests


def get_profs():

    r = requests.get("http://www.heb.be/esi/personnel_fr.htm")

    soup = BeautifulSoup(r.text)
    soup = soup.findAll('ul')[2]

    profs = {}

    for line in soup:
        line = str(line)

        if "profs" in line:
            abbr = line.split("(")[1].split(")")[0]
            prof = line.split(">")[2].split("<")[0]

            profs[abbr] = prof.decode('utf-8')


HOURS = [
 '08:15',
 '09:15',
 '10:30',
 '11:30',
 '12:30',
 '13:45',
 '14:45',
 '16:00',
 '17:00',
 ]

DAYS = {
 0: 'Lundi',
 1: 'Mardi',
 2: 'Mercredi',
 3: 'Jeudi',
 4: 'Vendredi',
 }

MONTHS = {
 'janvier'  : '01',
 'février'  : '02',
 'mars'     : '03',
 'avril'    : '04',
 'mai'      : '05',
 'juin'     : '06',
 'juillet'  : '07',
 'aout'     : '08',
 'septembre': '09',
 'octobre'  : '10',
 'novembre' : '11',
 'décembre' : '12',
 }

HOLIDAYS = {
    'Fête de la Communauté française': ['27/09/2014'],
    'Congé de Toussaint': ['27/10/2014', '28/10/2014', '29/10/2014', '30/10/2014', '31/10/2014'],
    'Congé de l’Armistice': ['11/11/2014'],
    'Vacances d’hiver': ['22/12/2014', '23/12/2014', '24/12/2014', '25/12/2014', '26/12/2014',
    '29/12/2014', '30/12/2014', '31/12/2014', '01/01/2015', '02/01/2015'],
    #'Congé de Carnaval': 
    'Vacances de printemps': ['06/04/2015', '07/04/2015', '08/04/2015', '09/04/2015', '10/04/2015',
    '13/04/2015', '14/04/2015', '15/04/2015', '16/04/2015', '17/04/2015'],
    'Fête du Travail': ['01/05/2015'],
    'Congé de l’Ascension': ['25/06/2015'],
}

PROFS = {
 'ADT': 'Alain Detaille',
 'ARO': 'Anne Rousseau',
 'ART': 'Anne Rayet',
 'BDL': 'Bénoni Delfosse',
 'BEJ': 'Jonas Beleho',
 'CIH': 'Yashar Cihan',
 'CLG': 'Christine Leignel',
 'CLR': 'Catherine Leruste',
 'CUV': 'Geneviève Cuvelier',
 'DNA': 'David Nabet',
 'DWI': 'Didier Willame',
 'EFO': 'Eric Fontaine',
 'EGR': 'Eric Georges',
 'ELV': 'Eytan Levy',
 'FPL': 'Frédéric Pluquet',
 'GVA': 'Gilles Van Assche',
 'HAL': 'Amine Hallal',
 'JCJ': 'Jean-Claude Jaumain',
 'JDM': 'Jacqueline De Mesmaeker',
 'JDS': 'Jérôme Dossogne',
 'JMA': 'Jean-Marc André',
 'LBC': 'Laurent Beeckmans',
 'MAP': 'Michel Applaincourt',
 'MBA': 'Monica Bastreghi',
 'MCD': 'Marco Codutti',
 'MHI': 'Mohamed Hadjili',
 'MWA': 'Moussa Wahid',
 'MWI': 'Michel Willemse',
 'NPX': 'Nicolas Pettiaux',
 'NVS': 'Nicolas Vansteenkiste',
 'PBT': 'Pierre Bettens',
 'PMA': 'Pantelis Matsos',
 'RPL': 'René-Philippe Legrand',
 'SRV': 'Frédéric Servais',
 'YPR': 'Yves Pierseaux',
 } 
