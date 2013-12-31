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
    chdir("pdf/")

    for files in listdir("."):
        if files.endswith(".pdf"):
            pdfs.append(files)

    return pdfs


def pdf_scrape(file):
    '''Convert pdf to xml'''

    with open(file) as u:
        xml = pdftoxml(u.read())

    with open(pdf + ".xml", "w") as w:
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


def matrix_to_ics(matrix_dict, begin, end):

    c = Calendar()
    hours = ["08:15", "09:15", "10:15", "10:30", "11:30", \
        "13:45", "14:45", "15:45", "16:00", "17:00", "18:00"]
    begin = arrow.get("{} {}".format(begin, hours[0]), 'DD-MM-YYYY HH:mm')

    # for each group
    for key in matrix_dict.keys():
        # for each day
        for i, day in enumerate(matrix_dict[key]):
            # for each course
            for j, course in enumerate(day):

                e = Event()

                if course != None:

                    #print(course)
                    #abb, prof, local = course.split()
                    abb = course
                    #print(abb, prof, local)

                    e.name = abb

                    # set begin hour
                    hour = int(hours[j].split(':')[0])
                    minute = int(hours[j].split(':')[1])
                    #print(hour, minute)
                    e.begin = begin.replace(hour=hour, minute=minute)

                    # set end hour
                    e.end = e.begin.replace(hours=+1)

                    c.events.append(e)

            # new day
            begin = begin.replace(days=+1)

            # new week
            if i % 7 == 0:
                begin = begin.replace(weeks=+1)


    with open('my.ics', 'w') as f:
        f.writelines(c)
        #print(c)


if __name__ == '__main__':

    pdfs = list_pdf()

    print("\nAll PDFs : " + str(pdfs) + "\n")

    for pdf in pdfs:

        pdf_scrape(pdf)

        with open(pdf + ".xml") as r:

            xml = r.readlines()

        blocks = xml_to_blocks(xml)
        matrix_dict = blocks_to_matrix_dict(blocks)
        begin_date, end_date = ics_dates(xml)
        #print(begin_date, end_date)
        #print(matrix_dict.keys())
        matrix_to_ics(matrix_dict, begin_date, end_date)