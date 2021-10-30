"""
Utility functions to extract data from Udemy course url
"""

from urllib.parse import urlparse, parse_qs
import requests
import re


def get_coupon_code(url):
    """
    Get coupon code
    :param url: (str)
    :return: coupon code (str)
    """
    u = urlparse(url)
    q = parse_qs(u.query, keep_blank_values=True)
    if 'couponCode' in q:
        coupon_code = q['couponCode'][0]
        return coupon_code
    return None


def get_course_id(url):
    """
    Get course ID
    :param url: (str)
    :return: course id (str)
    """
    txt = requests.get(url).text
    id_rx = re.compile('course-id=\"([0-9]+)\"')
    if id_rx.search(txt):
        course_id = id_rx.search(txt)[1]
        return course_id
    return None
