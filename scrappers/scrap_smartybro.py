"""
Scrapper for SmartyBro
"""

from udemy_validator.util import get_coupon_code
from udemy_validator.validator import validate
from scrappers.util import get_soup


def scrap_smartybro(site_url):
    print(f'Searching {site_url}')
    scrapped_courses = list()
    valid_courses = list()

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
                link = item.find("h2", {"class": "grid-tit"}).find("a", href=True)["href"]
                scrapped_courses.append(link)

    for course in scrapped_courses:
        try:
            course_soup = get_soup(course)
            class_info = {"class": "fasc-button fasc-size-xlarge fasc-type-flat"}
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

    return 0
