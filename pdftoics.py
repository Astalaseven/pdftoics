#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from operator import attrgetter
from constantes import DAYS
from BeautifulSoup import BeautifulSoup


class Course:

    def __init__(self):
        self.content = " "
        self.top = 0
        self.left = 0
        self.width = 0
        self.height = 0
        self.font = 0

    @property
    def h_center(self):
        return self.left + self.width / 2

    @property
    def v_center(self):
        return self.top + self.height / 2

    def __repr__(self):
        return "<Course>"


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def xml_to_blocks(xml):
    blocks = []

    for line in xml:

        if "text" in line:
            soup1 = BeautifulSoup(line)
            c = Course()

            c.content = soup1.find("text").text
            c.top = int(soup1.find("text")['top'])
            c.left = int(soup1.find("text")['left'])
            c.width = int(soup1.find("text")['width'])
            c.height = int(soup1.find("text")['height'])
            c.font = int(soup1.find("text")['font'])

            blocks.append(c)

    return blocks


def blocks_to_matrix(blocks):
    matrix = [
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
    ]

    days = sorted(blocks[:5], key=attrgetter('left'))
    times = sorted(blocks[-10:-1], key=attrgetter('top'))
    courses = blocks[5:-10]
    name = blocks[-1].content

    for course in courses:
        distance = 100000
        closest_day = None

        for i, day in enumerate(days):
            
            if abs(day.h_center - course.h_center) < distance:

                distance = abs(day.h_center - course.h_center)
                closest_day = i

        distance = 100000
        closest_hour = None

        for i, time in enumerate(times):

            if abs(time.v_center - course.v_center) < distance:
                distance = abs(time.v_center - course.v_center)
                closest_hour = i

        matrix[closest_day][closest_hour] = course.content

    return name, matrix


def blocks_to_matrix_dict(blocks):

    def palambda(x):
        x.content = striphtml(x.content).strip()
        return x

    blocks = map(palambda, blocks)
    blocks = filter(lambda x: x.font > 0, blocks)
    blocks = filter(lambda x: x.content != '', blocks)

    start, tables = 0, {}

    for i, block in enumerate(blocks):

        if block.font == 3:
            name, matrix = blocks_to_matrix(blocks[start:i + 1])
            tables[name] = matrix
            start = i+1

    return tables


def pp_group(matrix_dict, group):

    if not group in matrix_dict:
        raise ValueError('Not in matrix_dict, sorry')

    matrix = matrix_dict[group]

    for day, col in enumerate(matrix):

        print '=== {} ==='.format(DAYS[day])

        for course in col:
            
            if course:
                print course
            else:
                print '----'


if __name__ == '__main__':

    blocks = xml_to_blocks(xml)
    matrix_dict = blocks_to_matrix_dict(blocks)
    #matrix_to_ics(matrix_dict, begin_date, end_date)
    #print matrix_dict
    #pp_group(matrix_dict, '1GIR-132')


