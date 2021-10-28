from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup
from util import validate
import requests as req


def scrap_smart(site_url):
    print(f'Searching {site_url}')
    result_course_list = list()
    courses_list = list()
    smart = req.get(site_url).text
    smart_soup = BeautifulSoup(smart, 'html.parser')
    grid = smart_soup.find_all("div", {"class": "item"})
    for item in grid:
        tag_list = item.find_all("span", {"class": "tag-post"})
        for tag in tag_list:
            if "Programming" in tag.text:
                courses_list.append(item.find("h2", {"class": "grid-tit"}).find("a", href=True)["href"])

    for course in courses_list:
        try:
            course_html = req.get(course).text
            course_soup = BeautifulSoup(course_html, 'html.parser')
            class_info = {"class": "fasc-button fasc-size-xlarge fasc-type-flat"}
            url = course_soup.find("a", class_info, href=True)["href"]
            u = urlparse(url)
            query = parse_qs(u.query, keep_blank_values=True)
            coupon_code = query.get('couponCode')[0]
            result = url.split('?')[0]+"?couponCode="+coupon_code
            if validate(result):
                result_course_list.append(result)
            else:
                continue
        except Exception as e:
            print(f"Error getting course: {e}")
            continue
    return result_course_list
