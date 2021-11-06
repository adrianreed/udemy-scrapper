"""
Main script to call all scrappers
"""
import sys
import logging
from scrappers.scrap_couponsme import main as couponsme_main
from scrappers.scrap_smartybro import main as smartybro_main


def main():
    log_format = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(filename='myapp.log', format=log_format, level=logging.INFO)

    couponsme = "https://udemycoupons.me/"
    smartybro = "https://smartybro.com/category/udemy-coupon-100-off/"

    logging.info('Process: Starting.')
    couponsme_main(couponsme)
    smartybro_main(smartybro)
    logging.info('Process: Completed.')

    return 0


if __name__ == "__main__":
    sys.exit(main())
