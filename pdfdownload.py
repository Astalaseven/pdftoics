#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from BeautifulSoup import BeautifulSoup

username = "esi_id"
password = "esi_pass"
s = requests.Session()


def authenticate(username, password, s):

    payload = {'login': username, 'password': password}
    r = s.post("http://elearning.esi.heb.be/index.php", data=payload)


def get_timetable(s):

    url = "http://elearning.esi.heb.be/courses/R/"
    soup = BeautifulSoup(s.get(url).text)

    timetable = url + soup.find("table").find("td").find("td").findAll("a")[1]['href']
    soup = BeautifulSoup(s.get(timetable).text)

    return soup, timetable


def clean_url(url):

    url = ""

    for link in timetable.split("/")[:-1]:

        url += link + "/"

    return url


def save_pdf(url, directory, pdf, session):

    try:
        with open("pdf/" + directory + "/" + pdf, "wb") as p:

            r = session.get(url, stream=True)

            for block in r.iter_content(1024):

                if not block:
                    break

                p.write(block)
    except IOError:
        pass


if __name__ == '__main__':

    if username == "esi_id" or password == "esi_pass":

        print("Please enter your credentials. Quitting.")
        exit()


    authenticate(username, password, s)
    soup, timetable = get_timetable(s)
    pdfs = soup.findAll("a")

    for pdf in pdfs:

        pdf = pdf['href'].split("%2F")[-1]

        url = clean_url(timetable)
        url += pdf

        directory = url.split("/")[-2]
        if not os.path.exists("pdf/" + directory):
            os.makedirs("pdf/" + directory)

        if url.endswith(".pdf"):
            print("Downloading: " + pdf + " to pdf/" + directory)
            save_pdf(url, directory, pdf, s)




