"""
Main script to call all scrappers
"""
from udemy_validator.validator import validate
from scrappers.scrap_couponsme import main as couponsme_main
from scrappers.scrap_smartybro import main as smartybro_main
import logging

couponsme = "https://udemycoupons.me/"
smartybro = "https://smartybro.com/category/udemy-coupon-100-off/"


def logger(name, file, level=logging.INFO):

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler = logging.FileHandler(file, mode='w')
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    log = logging.getLogger(name)
    log.setLevel(level)
    log.addHandler(file_handler)
    log.addHandler(stream_handler)

    return log


def main():
    info = logger('info', 'info.log', level=logging.INFO)
    # debug = logger('debug', 'debug.log', level=logging.DEBUG)

    all_links = list()

    info.info('Process: Start scrapping.')
    all_links.extend(couponsme_main(couponsme))
    all_links.extend(smartybro_main(smartybro))
    info.info('Process: Scrapping completed.')

    info.info('Process: Start validations.')
    for li in all_links:
        result = validate(li)
        if not result["ok"]:
            info.info(result['message'])
            continue
        print(f'{li} expires in {result["exp_date"]}')
    info.info('Process: Validations completed.')

    return 0


if __name__ == "__main__":
    main()
