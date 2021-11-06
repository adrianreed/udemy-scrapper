"""
Scrapper for SmartyBro
"""
import logging
from udemy_validator.validator import validate
from util.get_site import get_site
from util.get_soup import get_soup
from util.threader import threader
from util.ud_url_parse import get_coupon_code


def scrap_site(url):
    """
    Get the list of courses in the landing page
    :param url: (str)
    :return: courses (set)
    """
    links = list()

    logging.info(f'Process: Start scrapping {url}')
    site = get_site(url)
    if not site['ok']:
        logging.warning(site["message"])
        return links

    text = site['site'].text
    soup = get_soup(text)
    if not soup['ok']:
        logging.warning(soup["message"])
        return links

    s = soup['soup']
    grid = s.find_all("div",
                      {"class": "item"}
                      )
    for i in grid:
        tags = i.find_all("span",
                          {"class": "tag-post"}
                          )
        for t in tags:
            if "Programming" in t.text:
                title = i.find("h2",
                               {"class": "grid-tit"}
                               )
                link = title.find("a", href=True)["href"]
                links.append(link)
    logging.info(f'Process: Done scrapping {url}')
    return links


def get_udemy_links(scrap_links):
    """
    Scan list of link sites' and extract Udemy links.
    :param scrap_links: (list)
    :return: valid Udemy links (list)
    """
    udemy_links = list()

    for li in scrap_links:
        logging.info(f'Process: Extracting Udemy link from: {li}.')

        site = get_site(li)
        if not site['ok']:
            logging.warning(site["message"])
            continue

        text = site['site'].text
        soup = get_soup(text)
        if not soup['ok']:
            logging.warning(soup["message"])
            continue

        s = soup['soup']
        try:
            course_url = s.find("a",
                                {"class": "fasc-button fasc-size-xlarge fasc-type-flat"},
                                href=True
                                )["href"]
        except Exception as e:
            logging.warning(f'Failed to get Udemy URL from {li}: {e}')
            continue

        coupon_code = get_coupon_code(course_url)
        if not coupon_code:
            logging.info(f'Failed to get coupon code for {li}')
            continue

        udemy_link = course_url.split('?')[0]+"?couponCode="+coupon_code
        if validate(udemy_link):
            udemy_links.append(udemy_link)

        logging.info(f'Process: Done extracting Udemy link from: {li}.')
    return udemy_links


def main(url):
    links = scrap_site(url)
    if len(links) != 0:
        threader(get_udemy_links, links)
    return
