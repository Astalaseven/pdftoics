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

PROFS = {
 'ADT': 'Alain Detaille',
 'ARO': 'Anne Rousseau',
 'ART': 'Anne Rayet',
 'BDL': 'B\xc3\xa9noni Delfosse',
 'BEJ': 'Jonas Beleho',
 'CIH': 'Yashar Cihan',
 'CLG': 'Christine Leignel',
 'CLR': 'Catherine Leruste',
 'CUV': 'Genevi\xc3\xa8ve Cuvelier',
 'DNA': 'David Nabet',
 'DWI': 'Didier Willame',
 'EFO': 'Eric Fontaine',
 'EGR': 'Eric Georges',
 'ELV': 'Eytan Levy',
 'FPL': 'Fr\xc3\xa9d\xc3\xa9ric Pluquet',
 'GVA': 'Gilles Van Assche',
 'HAL': 'Amine Hallal',
 'JCJ': 'Jean-Claude Jaumain',
 'JDM': 'Jacqueline De Mesmaeker',
 'JDS': 'J\xc3\xa9r\xc3\xb4me Dossogne',
 'JMA': 'Jean-Marc Andr\xc3\xa9',
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
 'RPL': 'Ren\xc3\xa9-Philippe Legrand',
 'SRV': 'Fr\xc3\xa9d\xc3\xa9ric Servais',
 'YPR': 'Yves Pierseaux',
 } 
