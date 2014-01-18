#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import arrow
from ics import Calendar, Event
from pdftoics import xml_to_blocks, blocks_to_matrix_dict
from scraperwiki import pdftoxml

def list_pdf():
    '''Lists all pdfs in subdirectory'''

    pdfs = {}
    directories = os.listdir("pdf/")

    for i in directories:
        pdfs[i] = []

    for directory in directories:
        for files in os.listdir("pdf/" + directory):
            if files.endswith(".pdf"):
                pdfs[directory].append(files)

    return pdfs


def pdf_scrape(pdf, directory):
    '''Convert pdf to xml'''

    with open("pdf/" + directory + "/" + pdf) as u:
        xml = pdftoxml(u.read())

    with open("xml/" + pdf + ".xml", "w") as w:
        w.write(xml)

    return xml


def ics_dates(xml):
    '''Get begin and end date'''

    for line in xml:

        if "Début" in line:
            begin = line.split(":")[1].split("<")[0]

        if "Fin" in line:
            end = line.split(":")[1].split("<")[0]
            break

    return begin, end


def matrix_to_ics(matrix_dict, group, begin, end, directory):

    c = Calendar()

    #print(c.events)

    hours = ["08:15", "09:15", "10:30", "11:30", "12:30", "13:45", "14:45", "16:00", "17:00"]

    d = {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 4: 'Vendredi'}

    # begin = arrow.get("{} {}".format(begin, hours[0]), 'DD-MM-YYYY HH:mm')
    months = {"janvier":'01', "février":'02', "mars":'03', "avril":'04', "mai":'05', "juin":'06', 
    "juillet":'07', "aout":'08', "septembre":'09', "octobre":'10', "novembre":'11', "décembre":'12'}

    day, month, year = begin.split(" ")
    begin = "{} {} {}".format(day, months[month], year)

    begin = arrow.get("{} {}".format(begin, hours[0]), 'DD MM YYYY HH:mm')


    # for each day
    for i, day in enumerate(matrix_dict[group]):
        # for each course
        for j, course in enumerate(day):

            e = Event()

            if course:

                e.name = course

                # get begin hour
                hour = int(hours[j].split(':')[0])
                minute = int(hours[j].split(':')[1])

                # set event begin/end date
                e.begin = begin.replace(hour=hour, minute=minute)
                e.end = e.begin.replace(hours=+1)

                c.events.append(e)

        # new day
        begin = begin.replace(days=+1)

    if not os.path.exists("ics/" + directory):
        os.makedirs("ics/" + directory)

    with open("ics/" + directory + "/" + group + ".ics", "w") as f:
        f.writelines(c)

def convert(directories, pdfs):

    for directory in directories:

        pdf = pdfs[directory]

        for p in pdf:

            pdf_scrape(p, directory)

            with open("xml/" + p + ".xml") as r:

                xml = r.readlines()

            blocks = xml_to_blocks(xml)
            matrix_dict = blocks_to_matrix_dict(blocks)
            begin_date, end_date = ics_dates(xml)

            # for each group
            for group in matrix_dict.keys():

                print(p, group)
                matrix_to_ics(matrix_dict, group, begin_date, end_date, directory)


if __name__ == '__main__':

    pdfs = list_pdf()
    #print(pdfs)
    directories = pdfs.keys()

    print("\nAll PDFs : " + str(pdfs) + "\n")

    convert(directories, pdfs)