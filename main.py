"""
Main script to call all scrappers
"""
import sys
import logging
from udemy_validator.validator import validate
from scrappers.scrap_couponsme import main as couponsme_main
from scrappers.scrap_smartybro import main as smartybro_main

couponsme = "https://udemycoupons.me/"
smartybro = "https://smartybro.com/category/udemy-coupon-100-off/"


def logger(name, file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler = logging.FileHandler(file, mode='w')
    file_handler.setFormatter(formatter)

    log = logging.getLogger(name)
    log.setLevel(level)
    log.addHandler(file_handler)

    return log


def main():
    info = logger('info', 'info.log', level=logging.DEBUG)

    all_links = list()

    info.info('Process: Start scrapping.')

    cm_result = couponsme_main(couponsme)
    if not cm_result:
        info.info('Failed to scan CouponsMe.')
    else:
        all_links.extend(cm_result)

    sb_result = smartybro_main(smartybro)
    if not sb_result:
        info.info('Failed to scan SmartyBro.')
    else:
        all_links.extend(sb_result)

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
    sys.exit(main())
