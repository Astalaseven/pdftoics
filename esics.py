#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arrow
from ics import Calendar, Event
from os import chdir, listdir
from pdftoics import xml_to_blocks, blocks_to_matrix_dict
from scraperwiki import pdftoxml

def list_pdf():
    '''Lists all pdfs in subdirectory'''

    pdfs = []

    for files in listdir("pdf/."):
        if files.endswith(".pdf"):
            pdfs.append(files)

    return pdfs


def pdf_scrape(file):
    '''Convert pdf to xml'''

    with open("pdf/" + file) as u:
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


def matrix_to_ics(matrix_dict, group, begin, end):

    c = Calendar()

    hours = ["08:15", "09:15", "10:30", "11:30", "12:30", "13:45", "14:45", "16:00", "17:00"]

    d = {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 4: 'Vendredi'}

    begin = arrow.get("{} {}".format(begin, hours[0]), 'DD-MM-YYYY HH:mm')


    # for each day
    for i, day in enumerate(matrix_dict[group]):
        # for each course
        for j, course in enumerate(day):

            print(d[i], hours[j], course)

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

                print(e)

        # new day
        begin = begin.replace(days=+1)

    with open("ics/" + group + ".ics", "w") as f:
        f.writelines(c)


if __name__ == '__main__':

    pdfs = list_pdf()

    print("\nAll PDFs : " + str(pdfs) + "\n")

    for pdf in pdfs:

        pdf_scrape(pdf)

        with open("xml/" + pdf + ".xml") as r:

            xml = r.readlines()

        blocks = xml_to_blocks(xml)
        matrix_dict = blocks_to_matrix_dict(blocks)
        begin_date, end_date = ics_dates(xml)
        #print(begin_date, end_date)
        #print(matrix_dict.keys())
        # for each group
        # for key in matrix_dict.keys():
        group = matrix_dict.keys()[0]
        print(group)
        matrix_to_ics(matrix_dict, group, begin_date, end_date)
        print("\n\n\n")