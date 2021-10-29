"""
Scrapper for SmartyBro
"""

from udemy_validator.util import get_coupon_code
from udemy_validator.validator import validate
from scrappers.util import get_soup, chunks
import threading


def scrap_smartybro(site_url):
    print(f'Searching {site_url}')

    scrapped_courses = landing_page_scrap(site_url)

    hilosLinks = list(
        chunks(scrapped_courses, int((len(scrapped_courses)/10)+1)))
    threads = []
    identificador = 0
    for x in range(0, 8):
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
        grid = soup.find_all("div", {"class": "item"})
    except Exception as e:
        print(f"Error getting {site_url}: {e}")
        return 1

    for item in grid:
        tags = item.find_all("span", {"class": "tag-post"})
        for t in tags:
            if "Programming" in t.text:
                link = item.find("h2", {"class": "grid-tit"}
                                 ).find("a", href=True)["href"]
                scrapped_courses.append(link)

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
            course_soup = get_soup(course)
            class_info = {
                "class": "fasc-button fasc-size-xlarge fasc-type-flat"}
            course_url = course_soup.find("a", class_info, href=True)["href"]
            coupon_code = get_coupon_code(course_url)
            result = course_url.split('?')[0]+"?couponCode="+coupon_code
        except Exception as e:
            print(f"Error processing {course}: {e}")
            continue
        if validate(result):
            valid_courses.append(result)
        else:
            continue
    return valid_courses
