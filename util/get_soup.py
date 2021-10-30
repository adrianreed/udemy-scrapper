from bs4 import BeautifulSoup


def get_soup(text):
    """
    Get soup from a site
    :param text: (str) requests.get().text attribute
    :return:
    """
    try:
        soup = BeautifulSoup(text, 'html.parser')
    except Exception as e:
        message = f'Error creating soup: {e}'
        return dict(
            ok=False,
            message=message
        )
    return dict(
        ok=True,
        soup=soup
    )
