import asyncio
import re
import requests
from bs4 import BeautifulSoup


def scrape_amazon_product_list(brand):
    # headers = (
    #     {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3", "Accept-Language":"en-US, en:q=0.5"},
    #     {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0", "Accept-Language":"en-US, en:q=0.5"}
    # )
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0", "Accept-Language":"en-US, en:q=0.5"}
    #1 get brand page
    brand_page=get_brand_page(brand, headers)
    #1 get brand page
    #2 get all products in brand page
    #3 get href of products
    #4 go to each product page
    #5 scrape product information
    #6 repeat from #4

    #2 get all products in brand page
    if brand_page.status_code == 200:
        soup = BeautifulSoup(brand_page.content, "html.parser")
    else:
        return f"Could not access {brand}".casefold() + "\n brand page may be available"
    products = []

    # Find all product containers (this selector may vary)
    product_links=soup.find_all('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    # print(product_links[0])

    for product in product_links:
        # print(product)
    # for i in range(1):
        # product=product_links[0]
        link = product.get('href')
        print(link)
        for a in range(200):
            pass
        product_link, product_page = get_product_page(link,headers)
        if product_page.status_code == 200:
            product_page = BeautifulSoup(product_page.content, "html.parser")
        else:
            return f"Could not access {product.split('/')[1]}".casefold() + "\n product page may be available"
        try:
            product_info = re.split('[/\\\\]', product_link)
            # name = product_page.find("span", {"class": "a-size-large product-title-word-break"}).get_text(strip=True)
            name = product_info[3]
            name = " ".join(re.split('[|,;-]',name))
            print("Name", name)
            asin = product_info[5]
            # asin = product_page.find("ul", {"class": "a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"}).find_all("li")[2].find("span", {"class": "a-list-item"}).find_all("span")[1].get_text(strip=True)
            # find_all("span", {"class": "a-list-item"})[1].get_text(strip=True)
            print("ASIN", asin)
            # sku = product_page.find("span", {"class": "sku"})  # This may vary by product or may not exist
            # sku = sku.get_text(strip=True) if sku else None
            image_url = product_page.find("ul", {"class":"a-unordered-list a-nostyle a-horizontal list maintain-height"}).find("img", {"class": "a-dynamic-image"})['src']
            print("image url", image_url)
            print(" ")
        except IndexError:
            continue
        products.append({
            'name': name,
            'asin': asin,
            # 'sku': sku,
            'image_url': image_url
        })
    return products

def get_brand_page(brand,headers):
    brand_url = "https://www.amazon.com/s?k=" + brand
    response = requests.get(brand_url, headers=headers)
    return response

def get_product_page(product_href,headers):
    # add protocol, domain and subdomain to only product links that don't have a full address
    if "https" not in product_href:
        product_url = "https://www.amazon.com" + product_href
    # handle links that have prefixes e.g. links of sponsored product posts
    else:
        product_url = "www.amazon.com" + product_href
        product_url = "https://www" + product_url.split("www")[-1]
    response = requests.get(product_url, headers=headers)
    return product_url, response

if __name__ == "__main__":
    import sys
    brand = sys.argv[1]
    print(scrape_amazon_product_list(brand))