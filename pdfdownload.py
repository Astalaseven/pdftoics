import requests
from BeautifulSoup import BeautifulSoup

user = "esi_id"
password = "esi_pass"
s = requests.Session()


def authenticate(user, password, s):

    payload = {'login': user, 'password': password}
    r = s.post("http://elearning.esi.heb.be/index.php", data=payload)


def get_timetable(s):

    url = "http://elearning.esi.heb.be/courses/R/"
    soup = BeautifulSoup(s.get(url).text)

    timetable = url + soup.find("table").find("td").find("td").find("a")['href']
    soup = BeautifulSoup(s.get(timetable).text)

    return soup, timetable


def clean_url(url):

    url = ""

    for link in timetable.split("/")[:-1]:

        url += link + "/"

    return url


def save_pdf(url, pdf, session):

    with open("pdf/" + pdf, "wb") as p:

        r = session.get(url, stream=True)

        for block in r.iter_content(1024):

            if not block:
                break

            p.write(block)


if __name__ == '__main__':

    if user == "esi_id" or password == "esi_pass":

        print("Please enter your credentials. Quitting.")
        exit()


    authenticate(user, password, s)
    soup, timetable = get_timetable(s)
    pdfs = soup.findAll("a")

    for pdf in pdfs:
        
        pdf = pdf['href']

        url = clean_url(timetable)
        url += pdf

        print("Downloading: " + pdf)
        save_pdf(url, pdf, s)




