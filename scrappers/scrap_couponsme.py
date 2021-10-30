"""
Scrapper for CouponsMe
"""
from util.get_soup import get_soup


def scrap_site(url):
    """
    Get list of links which site contains Udemy discount links.
    :param url: (str)
    :return courses: (set)
    """
    scrap_links = list()

    soup = get_soup(url)
    if soup['ok']:
        grid = soup['data'].find_all("a", {"rel": "bookmark"}, href=True)
        for i in grid:
            scrap_links.append(i["href"])
    else:
        print(soup.message)
        return 1
    return set(scrap_links)


def get_udemy_links(scrap_links):
    """
    Scan list of link sites' and extract Udemy links.
    :param scrap_links: (set)
    :return: Udemy links (list)
    """
    udemy_links = list()

    for li in scrap_links:
        soup = get_soup(li)
        if soup['ok']:
            item = soup['data'].find_all("a",
                                         {"target": "_blank"},
                                         href=True,
                                         text=True)
            for i in item:
                if '[ENROLL THE COURSE]' in i.text:
                    udemy_link = i["href"]
                    udemy_links.append(udemy_link)
        else:
            print(soup['message'])
            continue
    return udemy_links


def main(url):
    scraps = scrap_site(url)

    return get_udemy_links(scraps)
