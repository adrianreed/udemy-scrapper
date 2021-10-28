from scrap_couponsme import scrap_couponsme
from scrap_smartybro import scrap_smart

"""
Main script to call all scrappers
"""

site_couponsme = "https://udemycoupons.me/"
site_smartybro = "https://smartybro.com/category/udemy-coupon-100-off/"


def main():
    print('Calling all scrappers.')
    scrap_couponsme(site_couponsme)
    scrap_smart(site_smartybro)


if __name__ == "__main__":
    main()
