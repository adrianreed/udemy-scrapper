"""
Udemy coupon validator
"""

import requests as req
from udemy_validator.util import get_course_id, get_coupon_code


def validate(scrapper_link):
    """
    Validates coupon data to ensure it's usable
    :param scrapper_link: (str) Udemy course link retrieved from scrapper
    :return: (bool) True=valid False=invalid
    """
    course_id = get_course_id(scrapper_link)
    coupon_code = get_coupon_code(scrapper_link)

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
