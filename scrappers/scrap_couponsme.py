"""
Scrapper for CouponsMe
"""
from util.get_site import get_site
from util.get_soup import get_soup


def scrap_site(url):
    """
    Get list of links which site contains Udemy discount links.
    :param url: (str)
    :return courses: (set)
    """
    links = list()

    site = get_site(url)
    if not site['ok']:
        message = site["message"]
        return dict(
            ok=False,
            message=message
        )
    text = site['site'].text
    soup = get_soup(text)
    if not soup['ok']:
        message = soup["message"]
        return dict(
            ok=False,
            message=message
        )
    s = soup['soup']

    grid = s.find_all("a",
                      {"rel": "bookmark"},
                      href=True)
    for i in grid:
        links.append(i["href"])
    links = set(links)

    return dict(
        ok=True,
        links=links
    )


def get_udemy_links(scrap_links):
    """
    Scan list of link sites' and extract Udemy links.
    :param scrap_links: (set)
    :return: Udemy links (list)
    """
    udemy_links = list()

    for li in scrap_links:
        site = get_site(li)
        if not site['ok']:
            message = site["message"]
            return dict(
                ok=False,
                message=message
            )
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
                udemy_links.append(udemy_link)
            else:
                continue
    return udemy_links


def main(url):
    result = scrap_site(url)
    if not result['ok']:
        return False
    return get_udemy_links(result['links'])
