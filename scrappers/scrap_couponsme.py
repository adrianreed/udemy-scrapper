"""
Scrapper for CouponsMe
"""

from udemy_validator.validator import validate
from scrappers.util import get_soup


def scrap_couponsme(site_url):
    print(f'Searching {site_url}')
    valid_courses = list()
    scrapped_courses = list()

    try:
        soup = get_soup(site_url)
        grid = soup.find_all("a", {"rel": "bookmark"}, href=True)
    except Exception as e:
        print(f"Error getting {site_url}: {e}")
        return 1

    for item in grid:
        scrapped_courses.append(item["href"])

    scrapped_courses = list(dict.fromkeys(scrapped_courses))

    for course in scrapped_courses:
        try:
            soup = get_soup(course)
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
