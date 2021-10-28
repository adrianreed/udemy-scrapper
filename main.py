from bs4 import BeautifulSoup
import requests as req
from urllib.parse import urlparse, parse_qs
import re


def scrap_udemy_coupons():
    result_course_list = list()
    coupons_list = list()
    site_url = "https://udemycoupons.me/"
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
    

def scrap_smart():
    result_course_list = list() 
    courses_list = list()
    smart = req.get("https://smartybro.com/category/udemy-coupon-100-off/").text
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


def validate(udemy_link):
    txt = req.get(udemy_link).text
    id_rx = re.compile('course-id=\"([0-9]+)\"')
    course_id = id_rx.search(txt)[1]
    coupon_code = get_coupon_code(udemy_link)
    url_string = (f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}"
                  f"/me/?couponCode={coupon_code}&components=redeem_coupon,discount_expiration"
                  )
    validation = req.get(url_string).json()

    if all(k in validation for k in ("discount_expiration", "redeem_coupon")):
        coupon_enabled = validation["discount_expiration"]["data"]["is_enabled"]
        coupon_details = validation["redeem_coupon"]["discount_attempts"][0]["details"]
        if coupon_enabled and coupon_details is None:
            exp_date = validation["discount_expiration"]["data"]["discount_deadline_text"]
            print(f'{udemy_link} expires in {exp_date}')
            return True
        else:
            return False


def get_coupon_code(url):
    u = urlparse(url)
    query = parse_qs(u.query, keep_blank_values=True)
    return query.get('couponCode')[0]


def main():
    scrap_udemy_coupons()
    scrap_smart()


if __name__ == "__main__":
    main()
