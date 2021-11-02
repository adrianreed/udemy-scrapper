"""
Scrapper for CouponsMe
"""
import logging
from util.threader import threader
from udemy_validator.validator import validate
from util.get_site import get_site
from util.get_soup import get_soup

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file_handler = logging.FileHandler("scrap_couponsme.log", mode="w")
file_handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(file_handler)

def scrap_site(url):
    """
    Get list of links which site contains Udemy discount links.
    :param url: (str)
    :return courses: (set)
    """


    links = list()

    log.info("Start")
    site = get_site(url)
    if not site['ok']:
        log.error(site["message"])
        return links
    text = site['site'].text
    soup = get_soup(text)
    if not soup['ok']:
        log.error(soup["message"])
        return links
    s = soup['soup']

    grid = s.find_all("a",
                      {"rel": "bookmark"},
                      href=True)
    for i in grid:
        links.append(i["href"])
    links = list(set(links))

    return links
    

def get_udemy_links(scrap_links):
    """
    Scan list of link sites' and extract Udemy links.
    :param scrap_links: (set)
    :return: Udemy links (list)
    """
    udemy_links = list()

    for li in scrap_links:
        log.info(f"Start: {li}")
        site = get_site(li)
        if not site['ok']:
            log.error(site["message"])
            continue
        text = site['site'].text
        soup = get_soup(text)
        if not soup['ok']:
            continue
        s = soup['soup']
        item = s.find_all("a",
                          {"target": "_blank"},
                          href=True,
                          text=True)
        for i in item:
            if '[ENROLL THE COURSE]' in i.text:
                udemy_link = i["href"]
                if validate(udemy_link):
                    udemy_links.append(udemy_link)
            else:
                continue
    return udemy_links


def main(url):
    result = scrap_site(url)
    if len(result) == 0:
        return False
    return threader(result,get_udemy_links)
