import asyncio
import random
import re
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

def scrape_amazon_product_list(brand_name):
    main_headers = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3", "Accept-Language":"en-US, en:q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36", "Accept-Language":"en-US, en:q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept-Language":"en-US, en:q=0.5"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36", "Accept-Language":"en-US, en:q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0", "Accept-Language":"en-US, en:q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15", "Accept-Language":"en-US, en:q=0.5"}
    ]
    main_header = random.choice(main_headers)
    headers = scrape_user_agents("https://www.useragents.me/", main_header)
    proxies = get_proxies("https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text", main_header)
    if not headers:
        return None
    page_no = 1
    products = []

    while True:
        # print("Brand Page ", page_no)
        # 5 retries for brand page
        for _ in range(5):
            header = random.choice(headers)
            try:
                # 1 get brand page
                brand_page = get_brand_page(brand_name, header, str(page_no))

                #2 get all products in brand page
                if brand_page.status_code == 200:
                    soup = BeautifulSoup(brand_page.content, "html.parser")
                    # 3 get href of products
                    # Find all product containers (this selector may vary)
                    product_tags = soup.find_all('a', {
                        'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'
                    }
                                                 )
                    break
                else:
                    return products
            except:
                time.sleep(2)

        # pagination
        page_no += 1
        # 4 go to each product page
        for product_tag in product_tags:
            for _ in range(5):
                header = random.choice(headers)
                link = product_tag.get('href')
                # print(link)
                product_link, product_page = get_product_page(link,header)
                # if product_page.status_code == 200:
                product_page = BeautifulSoup(product_page.content, "html.parser")
                try:
                    # 5 scrape product information
                    product_info = re.split('[/\\\\]', product_link)
                    # name = product_page.find("span", {"class": "a-size-large product-title-word-break"}).get_text(strip=True)
                    name = product_info[3]
                    name = " ".join(re.split('[|,;-]',name))
                    # print("Name", name)
                    asin = product_info[5]
                    # print("ASIN", asin)
                    # sku = product_page.find("span", {"class": "sku"})  # This may vary by product or may not exist
                    page = product_link
                    # print("page", page)
                    image_url=product_page.find("div",{"class":"imgTagWrapper"}).find("img")['src']

                    # image_url = product_page.find("ul", {"class":"a-unordered-list a-nostyle a-horizontal list maintain-height"}).find("img")['src']
                    # print("image url", image_url)
                    # print(" ")
                    # update product information list
                    products.append({
                        'name': name,
                        'asin': asin,
                        'page': page,
                        'image_url': image_url
                    })
                    break
                except IndexError:
                    # print('Got Index Error')
                    time.sleep(2)
                except AttributeError:
                    # print('Got Attribute Error')
                    time.sleep(2)
            # 6 repeat from #4

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

def get_proxies(api, header):
    response = requests.get(api, headers=header)
    proxies = [proxy[:-1] for proxy in response.text.strip().split("\n") if 'http' in proxy]
    return proxies
