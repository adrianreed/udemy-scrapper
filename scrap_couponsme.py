from bs4 import BeautifulSoup
from util import validate
import requests as req


def scrap_couponsme(site_url):
    print(f'Searching {site_url}')
    result_course_list = list()
    coupons_list = list()
    header_data = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                   " AppleWebKit/537.36 (KHTML, like Gecko)"
                   " Chrome/95.0.4638.54"
                   " Safari/537.36")
    header = {"User-Agent": header_data}

    udemy_coupons = req.get(site_url, headers=header).text
    udemy_coupons_soup = BeautifulSoup(udemy_coupons, 'html.parser')
    grid = udemy_coupons_soup.find_all("a", {"rel": "bookmark"}, href=True)
    for item in grid:
        coupons_list.append(item["href"])
    coupons_list = list(dict.fromkeys(coupons_list))
    for course in coupons_list:
        try:
            course_html = req.get(course, headers=header).text
            course_soup = BeautifulSoup(course_html, 'html.parser')
            links = course_soup.find_all("a", {"target": "_blank"}, href=True, text=True)
            for link in links:
                if '[ENROLL THE COURSE]' in link.text:
                    udemy_link = link["href"]
                    if validate(udemy_link):
                        result_course_list.append(udemy_link)
        except Exception as e:
            print(f"Error getting course: {e}")
            continue
