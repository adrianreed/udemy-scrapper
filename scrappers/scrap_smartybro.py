"""
Scrapper for SmartyBro
"""
from util.get_site import get_site
from util.get_soup import get_soup
from util.ud_url_parse import get_coupon_code


def scrap_site(url):
    """
    Get the list of courses in the landing page
    :param url: (str)
    :return: courses (set)
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
        class_info = {"class": "fasc-button fasc-size-xlarge fasc-type-flat"}
        course_url = s.find("a", class_info, href=True)["href"]
        coupon_code = get_coupon_code(course_url)
        if not coupon_code:
            continue
        udemy_link = course_url.split('?')[0]+"?couponCode="+coupon_code
        udemy_links.append(udemy_link)

    return udemy_links


def main(url):
    result = scrap_site(url)
    if not result['ok']:
        return False
    return get_udemy_links(result['links'])
