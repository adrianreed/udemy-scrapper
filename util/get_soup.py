from bs4 import BeautifulSoup
import requests


def get_soup(url):
    """
    Get soup object from url.
    :param url: (str)
    :return: soup (obj)
    """

    h_data = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
              " AppleWebKit/537.36 (KHTML, like Gecko)"
              " Chrome/95.0.4638.54"
              " Safari/537.36")
    header = {"User-Agent": h_data}

    try:
        text = requests.get(url, headers=header).text
        soup = BeautifulSoup(text, 'html.parser')
    except Exception as e:
        msg = f'Error getting {url}: {e}'
        return dict(
            ok=False,
            message=msg
        )
    return dict(
        ok=True,
        message=f'{url} parsed successfully.',
        data=soup
    )
