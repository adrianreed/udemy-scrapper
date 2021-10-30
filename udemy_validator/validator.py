"""
Udemy coupon validator
"""
import requests
from util.ud_url_parse import get_course_id, get_coupon_code


def validate(link):
    """
    Validates coupon data to ensure it's usable
    :param link: (str) Udemy course link retrieved from scrapper
    :return: (dict) ok: (bool) valid/invalid link
                    exp_date: (str) if True
                    message: (str) if False
    """
    course_id = get_course_id(link)
    coupon_code = get_coupon_code(link)

    if all(x is not None for x in (course_id, coupon_code)):
        url_string = (f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}"
                      f"/me/?couponCode={coupon_code}&components=redeem_coupon,discount_expiration"
                      )
    else:
        return dict(
            ok=False,
            message=f'Invalid link: {link}. Failed to get coupon code or course id.'
        )

    try:
        json = requests.get(url_string).json()
    except Exception as e:
        return dict(
            ok=False,
            message=f'Failed to get {url_string}: {e}.'
        )

    if all(x in json for x in ("discount_expiration", "redeem_coupon")):
        # Bool, means coupon is enabled
        enabled = json["discount_expiration"]["data"]["is_enabled"]
        # If there's details, coupon is not valid
        details = json["redeem_coupon"]["discount_attempts"][0]["details"]
        # Valid coupons got expiration date info
        exp_date = json["discount_expiration"]["data"]["discount_deadline_text"]

        if not enabled:
            return dict(
                ok=False,
                message=f'Invalid link: {link}. Coupon not enabled.'
            )
        elif details is not None:
            return dict(
                ok=False,
                message=f'Invalid link: {link}. {details}'
            )
        elif not exp_date:
            return dict(
                ok=False,
                message=f'Invalid link: {link}. Failed to get expiration date.'
            )
        else:
            return dict(
                ok=True,
                exp_date=exp_date
            )
    else:
        return dict(
            ok=False,
            message=f'{link} may be already free. Link missing discount_expiration and data redeem_coupon data.'
        )
