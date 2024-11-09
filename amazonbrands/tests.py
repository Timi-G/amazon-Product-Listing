from django.test import TestCase

from amazonbrands.scraper import get_brand_page, get_product_page

HEADER={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3", "Accept-Language":"en-US, en:q=0.5"}

# Create your tests here.
class ScraperTest(TestCase):
    def test_brand_url(self):
        brand_url = get_brand_page("nike", HEADER)
        self.assertEqual(brand_url.status_code,200)

    def test_product_url(self):
        for i in range(100):
            pass
        product_url = get_product_page('Nike-Sportswear-Fleece-Windrunner-Full-Zip/dp/B0C9R5MFG5/ref=sr_1_6?dib=eyJ2IjoiMSJ9.Q1OIJrXk0am0xLOp7o4rkNl-ACEhy7UsgZqsNniZyvsXuYJ10GPNy-Yd4EVSnigLJUome2cct-6ySGWkoJ5TiHXAuDsFzSrwYno8DkFB0uvR1HZUQO0g1Ni5eb0c9AAk_O8m3bB25sQJLhCMo2iuEKAvYvqxxpXMMk4JApANriobG4DiTQLsukhfZZB_lndX1jun9Fkg2L6D-evk7mbLuGEcqwCjAdn6MuKziKaOVcy_nDIs8Rypfv-9RUceXjuAhBL668TqkLneE2o3abIqe2mE2ocURd_aMl-_ByB0qOc.40hM4A6zv8G6VBbc07ZO81hAWlKCO3BUhj17TL57okI&dib_tag=se&keywords=nike&qid=1730106177&sr=8-6', HEADER)
        self.assertEqual(product_url.status_code,200)

