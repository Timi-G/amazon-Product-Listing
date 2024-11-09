import asyncio
import random
import re
import urllib.parse

# import django
import requests
from bs4 import BeautifulSoup

# import os
#
# # Set up the Django settings module
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amazonProductListing.settings")
# django.setup()

from amazonbrands.models import Brand, Product


def scrape_amazon_product_list(brand_name):
    # headers = (
    #     {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3", "Accept-Language":"en-US, en:q=0.5"},
    #     {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0", "Accept-Language":"en-US, en:q=0.5"}
    # )
    main_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0", "Accept-Language":"en-US, en:q=0.5"}
    headers = scrape_user_agents("https://www.useragents.me/", main_header)
    if not headers:
        return None
    page_no = 1
    products = []

    while True:
        # headers = [ {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.3"},
        #             {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.3"},
        #             {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.1"},
        #             {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0", "Accept-Language":"en-US, en:q=0.5"}
        #            ]
        print("Brand Page ", page_no)
        # 5 retries for brand page
        for _ in range(5):
            header = random.choice(headers)
            brand_page = get_brand_page(brand_name, header, str(page_no))
            #1 get brand page
            #2 get all products in brand page
            #3 get href of products
            #4 go to each product page
            #5 scrape product information
            #6 repeat from #4

            #2 get all products in brand page
            if brand_page.status_code == 200:
                soup = BeautifulSoup(brand_page.content, "html.parser")
                break
            else:
                print(products)
                # get brand from database or create if not exist
                brand, created = Brand.objects.get_or_create(name=brand_name)
                for product in products:
                    # Save the product data to the database or take any required action
                    asin = product.get('asin')

                    # Check if a product with this ASIN already exists
                    if not Product.objects.filter(asin=asin, brand=brand).exists():
                        # If it doesn't exist, create a new product entry
                        new_product = Product.objects.create(
                            name=product.get('name'),
                            asin=asin,
                            page=product.get('page'),
                            image=product.get('image_url'),
                            brand=brand
                        )
                        new_product.save()
                # exit function
                return products

                # return f"Status Code is {brand_page.status_code}.\nCould not access " + f"{brand_name} ".capitalize() + "\nBrand page may be available"
        # 1 get brand page
        page_no += 1

        # Find all product containers (this selector may vary)
        product_tags = soup.find_all('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        # print(product_links[0])

        for product_tag in product_tags:
            header = random.choice(headers)
            link = product_tag.get('href')
            print(link)
            product_link, product_page = get_product_page(link,header)
            if product_page.status_code == 200:
                product_page = BeautifulSoup(product_page.content, "html.parser")
                # return "Could not access " + f"{product.split('/')[1]} ".capitalize() + "\n Product page may be available"
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
                page = product_link
                print("page", page)
                image_url = product_page.find("ul", {"class":"a-unordered-list a-nostyle a-horizontal list maintain-height"}).find("img")['src']
                print("image url", image_url)
                print(" ")

                # update product information list
                products.append({
                    'name': name,
                    'asin': asin,
                    'page': page,
                    'image_url': image_url
                })
            except IndexError:
                continue
            except AttributeError:
                continue


def extract_https_url(link):
    # Parse the URL to access its query parameters
    parsed_url = urllib.parse.urlparse(link)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # Retrieve the 'url' parameter and decode it to get the full URL
    if 'url' in query_params:
        encoded_url = query_params['url'][0]
        decoded_url = urllib.parse.unquote(encoded_url)

        # Convert the decoded relative URL to an absolute one with https
        full_url = urllib.parse.urljoin("https://www.amazon.com", decoded_url)
        return full_url
    else:
        return None  # Return None if 'url' parameter is not found


# Example usage
link = "/sspa/click?ie=UTF8&spc=MTo0NTA2ODczNTMyNDUyMjg3OjE3MzEwMzUzMTc6c3BfbXRmOjMwMDE2Nzg3ODk0OTYwMjo6MDo6&url=%2FDAILY-LAB-Freshener-Fragrance-Diffuser%2Fdp%2FB0BBGXP8L8%2Fref%3Dsr_1_62_sspa%3Fdib%3DeyJ2IjoiMSJ9.0FXKduWbm88Y_SBbaOS3fmTwC1fmE4fiyJ2bOPpa_pWySBLB-BL71wrsDXmIrm6b03DGCs7CVqDg728SQf7UU2OaShJIFCpFjZ01B_rexdfatn8OesWR7zkKNC3D4ssd2MxsjezEddVJHs-wWBDmqAGZR1orv6K1RSGyYWQtNKnulFTcd_WqpS2MSfo_nVERCUatxkZRVxfYc4quKEb4VC7Ved4WdZojFQ8nzKitAJtsU7oZtsE6ksGeSOt5l1zOwOuPLfhFZHeHAXI758_wS5u7W1pDl1JksQv33pTf56g.cXXJUu5Fd7Cth-l-vSh-fG8cMOB-kwpETDZyPDlZtxc%26dib_tag%3Dse%26keywords%3DTesla%26qid%3D1731035317%26sr%3D8-62-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9tdGY%26psc%3D1"
result = extract_https_url(link)
print(result)


def get_brand_page(brand,header,page_no):
    brand_url = "https://www.amazon.com/s?k=" + brand + "&page=" + page_no
    response = requests.get(brand_url, headers=header)
    return response

def get_product_page(product_href,headers):
    # add protocol, domain and subdomain to only product links that don't have a full address
    if "sspa" in product_href:
        product_url = extract_https_url(product_href)
    elif "aax-us-iad" in product_href:
        product_url = "www.amazon.com" + product_href
        product_url = "https://www" + product_url.split("www")[-1]
    else:
        # product_url = extract_https_url(product_href)
        product_url = "https://www.amazon.com" + product_href
    # handle links that have prefixes e.g. links of sponsored product posts
    response = requests.get(product_url, headers=headers)
    return product_url, response

def scrape_user_agents(page_url, header):
    response = requests.get(page_url, headers=header)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        user_agents_tag = soup.find_all("textarea",{"class": "form-control ua-textarea"})
    else:
        return []
    user_agents = [{"User-Agent": user_agent.get_text(strip=True), "Accept-Language":"en-US, en:q=0.5"} for user_agent in user_agents_tag]
    return user_agents

if __name__ == "__main__":
    # import sys
    # brand = sys.argv[1]
    print(scrape_amazon_product_list("tesla"))

    # header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0", "Accept-Language":"en-US, en:q=0.5"}
    # print(scrape_user_agents("https://www.useragents.me/",header))
