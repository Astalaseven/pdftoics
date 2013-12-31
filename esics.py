#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def matrix_to_ics():
    hours = ["8h15", "9h15", "10h15", "10h30", "11h30", "13h45", "14h45", "15h45", "16h", "17h", "18h"]
    for key in matrix_dict.keys():
        for day in matrix_dict[key]:
            for course in day:
                if course:
                    abb, prof, local = course.split()
                    print(abb, prof, local)


if __name__ == '__main__':

    pdfs = list_pdf()

    print("\nAll PDFs : " + str(pdfs) + "\n")

    for pdf in pdfs:

        pdf_scrape(pdf)

        with open(pdf + ".xml") as r:
            print("\nOuverture du fichier XML " + pdf + ".xml\n")
            xml = r.readlines()

        blocks = xml_to_blocks(xml)
        matrix_dict = blocks_to_matrix_dict(blocks)
        begin_date, end_date = ics_dates(xml)
        print(begin_date, end_date)
        print(matrix_dict.keys())