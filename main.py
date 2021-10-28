from bs4 import BeautifulSoup
import requests as req
from urllib.parse import urlparse, parse_qs
import re

# "https://udemycoupons.me/"

coursesList = list()
smart = req.get("https://smartybro.com/category/udemy-coupon-100-off/").text
smart_soup = BeautifulSoup(smart, 'html.parser')
grid = smart_soup.find_all("div", {"class": "item"})


def main():
    for item in grid:
        tag_list = item.find_all("span", {"class": "tag-post"})
        for tag in tag_list:
            if "Programming" in tag.text:
                coursesList.append(item.find("h2", {"class": "grid-tit"}).find("a", href=True)["href"])

    for course in coursesList:
        try:
            course_html = req.get(course).text
            course_soup = BeautifulSoup(course_html, 'html.parser')
            url = course_soup.find("a", {"class": "fasc-button fasc-size-xlarge fasc-type-flat"}, href=True)["href"]
            u = urlparse(url)
            query = parse_qs(u.query, keep_blank_values=True)
            coupon_code = query.get('couponCode')[0]
            result = url.split('?')[0]+"?couponCode="+coupon_code
            txt = req.get(result).text
            course_id = re.search("course-id=\"([0-9]+)\"", txt)[1]
            url_string = (f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}"
                          f"/me/?couponCode={coupon_code}&components=redeem_coupon,discount_expiration"
                          )
            validation = req.get(url_string).json()

            if all(k in validation for k in ("discount_expiration", "redeem_coupon")):
                coupon_enabled = validation["discount_expiration"]["data"]["is_enabled"]
                coupon_details = validation["redeem_coupon"]["discount_attempts"][0]["details"]
                if coupon_enabled and coupon_details is None:
                    exp_date = validation["discount_expiration"]["data"]["discount_deadline_text"]
                    print(f'{result} expires in {exp_date}')
            else:
                continue
        except Exception as e:
            print(f"Error getting course: {e}")
            continue
    return


if __name__ == "__main__":
    main()
