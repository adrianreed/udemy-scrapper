"""
Utility functions for scrapper modules
"""

from bs4 import BeautifulSoup
import requests as req

def get_soup(url):
    """
    Get soup object from url
    :param url: (str)
    :return: soup (obj)
    """

    h_data = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
              " AppleWebKit/537.36 (KHTML, like Gecko)"
              " Chrome/95.0.4638.54"
              " Safari/537.36")
    header = {"User-Agent": h_data}

    text = req.get(url, headers=header).text
    soup = BeautifulSoup(text, 'html.parser')
    return soup

