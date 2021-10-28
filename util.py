from urllib.parse import urlparse, parse_qs
import requests as req
import re


def validate(scrapper_link):
    # Get course ID
    course_id = get_course_id(scrapper_link)
    # Get coupon code
    coupon_code = get_coupon_code(scrapper_link)
    # Validate
    url_string = (f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}"
                  f"/me/?couponCode={coupon_code}&components=redeem_coupon,discount_expiration"
                  )
    validation = req.get(url_string).json()

    if all(k in validation for k in ("discount_expiration", "redeem_coupon")):
        coupon_enabled = validation["discount_expiration"]["data"]["is_enabled"]
        coupon_details = validation["redeem_coupon"]["discount_attempts"][0]["details"]
        if coupon_enabled and coupon_details is None:
            exp_date = validation["discount_expiration"]["data"]["discount_deadline_text"]
            print(f'{scrapper_link} expires in {exp_date}')
            return True
        else:
            return False


def get_coupon_code(url):
    u = urlparse(url)
    query = parse_qs(u.query, keep_blank_values=True)
    return query.get('couponCode')[0]


def get_course_id(url):
    txt = req.get(url).text
    id_rx = re.compile('course-id=\"([0-9]+)\"')
    return id_rx.search(txt)[1]
