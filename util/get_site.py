import requests


def get_site(url, headers=None):
    """
    Get request for a site.
    :param url: (str)
    :param headers: (dict)
    :return:
    """
    if headers is None:
        h_data = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/95.0.4638.54"
                  " Safari/537.36")
        headers = {"User-Agent": h_data}

    try:
        site = requests.get(url, headers=headers)
    except Exception as e:
        message = f'Error getting {url}: {e}'
        return dict(
            ok=False,
            message=message
        )
    return dict(
        ok=True,
        site=site
    )
