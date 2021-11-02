"""
Udemy coupon validator
"""
from util.get_site import get_site
import logging
from util.ud_url_parse import get_course_id, get_coupon_code


def validate(link):
    """
    Validates coupon data to ensure it's usable
    :param link: (str) Udemy course link retrieved from scrapper
    :return: (dict) ok: (bool) valid/invalid link
                    exp_date: (str) if True
                    message: (str) if False
    """
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler = logging.FileHandler("validator.log", mode="w")
    file_handler.setFormatter(formatter)

    log = logging.getLogger(__name__)
    log.addHandler(file_handler)
    
    course_id = get_course_id(link)
    coupon_code = get_coupon_code(link)
    log.debug(f"validation of: {link}")
    if all(x is not None for x in (course_id, coupon_code)):
        url_string = (f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}"
                      f"/me/?couponCode={coupon_code}&components=redeem_coupon,discount_expiration"
                      )
    else:
        log.error(f"Invalid link: {link}. Failed to get coupon code or course id.")
        return False

    site = get_site(url_string, headers={})
    if not site["ok"]:
        log.error( site["message"])
        return False

    json = site["site"].json()

    if all(x in json for x in ("discount_expiration", "redeem_coupon")):
        # Bool, means coupon is enabled
        enabled = json["discount_expiration"]["data"]["is_enabled"]
        # If there's details, coupon is not valid
        details = json["redeem_coupon"]["discount_attempts"][0]["details"]
        # Valid coupons got expiration date info
        exp_date = json["discount_expiration"]["data"]["discount_deadline_text"]

        if not enabled:
            log.error(f"Invalid link: {link}. Coupon not enabled.")
            return False
            
        elif details is not None:
            log.error(f"Invalid link: {link}. {details}")
            return False
        elif not exp_date:
            log.error(f"Invalid link: {link}. Failed to get expiration date.")
            return False
        else:
            log.info(f"{link} expires in {exp_date}")
            print(f"{link} expires in {exp_date}")
            return True 
    else:
        log.error(f"{link} may be already free. Link missing discount_expiration and data redeem_coupon data.")
        return False
