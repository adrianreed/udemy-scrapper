"""
Scrapper for CouponsMe
"""

from bs4 import BeautifulSoup
import requests as req
from udemy_validator.validator import validate


def scrap_couponsme(site_url):
    print(f'Searching {site_url}')
    valid_courses = list()
    scrapped_courses = list()

    h_data = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
              " AppleWebKit/537.36 (KHTML, like Gecko)"
              " Chrome/95.0.4638.54"
              " Safari/537.36")
    header = {"User-Agent": h_data}
    try:
        text = req.get(site_url, headers=header).text
        soup = BeautifulSoup(text, 'html.parser')
        grid = soup.find_all("a", {"rel": "bookmark"}, href=True)
    except Exception as e:
        print(f"Error getting {site_url}: {e}")
        return 1

    for item in grid:
        scrapped_courses.append(item["href"])

    for course in scrapped_courses:
        try:
            text = req.get(course, headers=header).text
            soup = BeautifulSoup(text, 'html.parser')
            links = soup.find_all("a", {"target": "_blank"}, href=True, text=True)
            for link in links:
                if '[ENROLL THE COURSE]' in link.text:
                    udemy_link = link["href"]
                    if validate(udemy_link):
                        valid_courses.append(udemy_link)
        except Exception as e:
            print(f"Error getting {course}: {e}")
            continue

    return 0
