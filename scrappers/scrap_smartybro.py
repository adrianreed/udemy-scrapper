"""
Scrapper for SmartyBro
"""
import logging
from udemy_validator.validator import validate
from util.get_site import get_site
from util.get_soup import get_soup
from util.threader import threader
from util.ud_url_parse import get_coupon_code

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file_handler = logging.FileHandler("scrap_couponsme.log", mode="w")
file_handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(file_handler)

def scrap_site(url):
    """
    Get the list of courses in the landing page
    :param url: (str)
    :return: courses (set)
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

    grid = s.find_all("div", {"class": "item"})
    for i in grid:
        tags = i.find_all("span", {"class": "tag-post"})
        for t in tags:
            if "Programming" in t.text:
                title = i.find("h2",
                               {"class": "grid-tit"}
                               )
                link = title.find("a", href=True)["href"]
                links.append(link)

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
        class_info = {"class": "fasc-button fasc-size-xlarge fasc-type-flat"}
        course_url = s.find("a", class_info, href=True)["href"]
        coupon_code = get_coupon_code(course_url)
        if not coupon_code:
            continue
        udemy_link = course_url.split('?')[0]+"?couponCode="+coupon_code
        if validate(udemy_link):
            udemy_links.append(udemy_link)

    return udemy_links


def main(url):
    result = scrap_site(url)
    if len(result) == 0:
        return False
    return threader(result,get_udemy_links)
