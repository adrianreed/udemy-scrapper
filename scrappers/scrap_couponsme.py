"""
Scrapper for CouponsMe
"""

from udemy_validator.validator import validate
from scrappers.util import get_soup, chunks
import threading


def scrap_couponsme(site_url):
    print(f'Searching {site_url}')

    scrapped_courses = landing_page_scrap(site_url)
    hilosLinks = list(
        chunks(scrapped_courses, int((len(scrapped_courses)/10)+1)))
    threads = []
    identificador = 0
    for x in range(0, 9):
        threads.append(threading.Thread(
            target=courses_scrapping, args=(hilosLinks[x],)))
        identificador = identificador+1
        pass
    for x in threads:
        x.start()
        pass
    for x in threads:
        x.join()
        pass

    return 0


def landing_page_scrap(site_url):
    """
    Get the list of courses in the landing page
    :param site_url: (str)
    :return: scrapped_courses (list)
    """
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
    return scrapped_courses


def courses_scrapping(scrapped_courses):
    """
    Get the list of validated courses
    :param scrapped_courses: (list)
    :return: valid_courses (list)
    """
    valid_courses = list()
    for course in scrapped_courses:
        try:
            soup = get_soup(course)
            links = soup.find_all(
                "a", {"target": "_blank"}, href=True, text=True)
            for link in links:
                if '[ENROLL THE COURSE]' in link.text:
                    udemy_link = link["href"]
                    if validate(udemy_link):
                        valid_courses.append(udemy_link)
        except Exception as e:
            print(f"Error getting {course}: {e}")
            continue
    return valid_courses
