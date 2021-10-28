"""
Utility functions for the Udemy validator
"""

from urllib.parse import urlparse, parse_qs
import requests as req
import re


def get_coupon_code(url):
    """
    Get coupon code from Udemy course url
    :param url: (str)
    :return: coupon code (str)
    """
    u = urlparse(url)
    query = parse_qs(u.query, keep_blank_values=True)
    return query.get('couponCode')[0]


def get_course_id(url):
    """
    Get course ID from Udemy course url
    :param url: (str)
    :return: course id (str)
    """
    txt = req.get(url).text
    id_rx = re.compile('course-id=\"([0-9]+)\"')
    return id_rx.search(txt)[1]
