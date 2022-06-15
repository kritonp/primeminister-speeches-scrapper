import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_year(speech_url):
    return speech_url.split("/")[-4]


def get_month(speech_url):
    return speech_url.split("/")[-3]


def get_day(speech_url):
    return speech_url.split("/")[-2]


def get_id(speech_url):
    return speech_url.split("/")[-1]


def create_date(speech_url):
    """
    :param speech_url: fetch url
    :return: YYYY-MM-DD
    """
    return str(get_year(speech_url)+'-'+get_month(speech_url)+"-"+get_day(speech_url))


def get_archive_urls(url):
    """
    :param url: fetch url
    :return: Retrieve archive urls per month
    """
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    options_list = soup.findAll('option')
    archive_url = []
    for option in options_list:
        archive_url.append(option['value'])
    return archive_url


def parse_single_url(speech_url):
    page = urlopen(speech_url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string
    id = get_id(speech_url)
    date = create_date(speech_url)

    # getting all the paragraphs
    text = ''
    for para in soup.find_all("p"):
        text = text + ' ' + para.get_text()

    data = [date, id, speech_url, title, text]
    return data


def read_log_file(filename):
    with open(filename) as f:
        links = f.read().splitlines()
    return links
