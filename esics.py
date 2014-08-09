#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import arrow
from ics import Calendar, Event
from ics.utils import uid_gen
from pdftoics import xml_to_blocks, blocks_to_matrix_dict
from constantes import HOURS, MONTHS, PROFS, HOLIDAYS
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

    if not os.path.exists("xml"):
        os.mkdir("xml")

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

def convert_holidays():
    holidays = []
    for holiday in HOLIDAYS.values():
        for date in holiday:
            holidays.append(arrow.get(date, 'DD/MM/YYYY').date())

    return holidays

def matrix_to_ics(matrix_dict, group, begin, end, directory):
    c = Calendar()

    day, month, year = begin.split(" ")
    begin = "{} {} {}".format(day if int(day) > 9 else '0%s' % (day), MONTHS[month], year)

    day, month, year = end.split(" ")
    end = "{} {} {}".format(day if int(day) > 9 else '0%s' % (day), MONTHS[month], year)

    begin = arrow.get("{} {}".format(begin, HOURS[0]), 'DD MM YYYY HH:mm')
    end = arrow.get("{} {}".format(end, HOURS[-1]), 'DD MM YYYY HH:mm')

    # for each day of the week
    for i, day in enumerate(matrix_dict[group]):
        # for each course of the day
        for j, course in enumerate(day):

            if course:
                # get begin hour
                hour = int(HOURS[j].split(':')[0])
                minute = int(HOURS[j].split(':')[1])

                e = Event()

                e.name = course
                e.begin = begin.replace(hour=hour, minute=minute)
                e.end = e.begin.replace(hours=+1)

                c.events.append(e)

                while (e.begin <= end):
                    e = e.clone()

                    e.end = e.end.replace(days=+7)
                    e.begin = e.begin.replace(days=+7)
                    e.uid = uid_gen()

                    c.events.append(e)

        # next day
        begin = begin.replace(days=+1)

    holidays = convert_holidays()
    for event in c.events:
        for date in holidays:
            if str(event.begin.date()) == str(date):
                c.events.remove(event)

    if not os.path.exists("ics/" + directory):
        os.makedirs("ics/" + directory)

    with open('ics/{}/{}.ics'.format(directory, group), 'w') as f:
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

def fix_timezone():

    def list_ics():
        '''Lists all ics in subdirectory'''
        ics = {}
        directories = os.listdir("ics/")

        for i in directories:
            ics[i] = []

        for directory in directories:
            for files in os.listdir("ics/" + directory):
                if files.endswith(".ics"):
                    ics[directory].append(files)

        return ics

    icss = list_ics()
    directories = icss.keys()

    for directory in directories:
        files = icss[directory]
        for ics in files:
            with open('ics/' + directory + '/' + ics, 'r') as f:
                content = f.readlines()
            content.insert(3, 'X-WR-TIMEZONE:Etc/GMT\n')

            with open('ics/' + directory + '/' + ics, 'w') as f:
                f.writelines(content)

if __name__ == '__main__':

    pdfs = list_pdf()
    directories = pdfs.keys()

    print("\nAll PDFs : " + str(pdfs) + "\n")

    convert(directories, pdfs)

    # hack to use correct timezone
    # fix_timezone()
