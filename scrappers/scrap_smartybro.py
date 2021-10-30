"""
Scrapper for SmartyBro
"""

from util.ud_url_parse import get_coupon_code
from util.get_soup import get_soup


def scrap_site(url):
    """
    Get the list of courses in the landing page
    :param url: (str)
    :return: courses (set)
    """
    scrap_links = list()

    soup = get_soup(url)
    if soup['ok']:
        grid = soup['data'].find_all("div", {"class": "item"})
        for i in grid:
            tags = i.find_all("span", {"class": "tag-post"})
            for t in tags:
                if "Programming" in t.text:
                    title = i.find("h2",
                                   {"class": "grid-tit"}
                                   )
                    link = title.find("a", href=True)["href"]
                    scrap_links.append(link)
    else:
        print(soup['message'])
        return 1
    return scrap_links


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
            class_info = {"class": "fasc-button fasc-size-xlarge fasc-type-flat"}
            course_url = soup['data'].find("a", class_info, href=True)["href"]
            coupon_code = get_coupon_code(course_url)
            udemy_link = course_url.split('?')[0]+"?couponCode="+coupon_code
            udemy_links.append(udemy_link)
        else:
            print(soup['message'])
            continue
    return udemy_links


def main(url):
    scraps = scrap_site(url)

    return get_udemy_links(scraps)
