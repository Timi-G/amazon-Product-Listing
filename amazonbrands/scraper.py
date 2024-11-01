import asyncio
import random
import re
import requests
from bs4 import BeautifulSoup


def scrape_amazon_product_list(brand):
    # headers = (
    #     {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3", "Accept-Language":"en-US, en:q=0.5"},
    #     {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0", "Accept-Language":"en-US, en:q=0.5"}
    # )
    main_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0", "Accept-Language":"en-US, en:q=0.5"}
    headers = scrape_user_agents("https://www.useragents.me/", main_header)
    if not headers:
        return None
    page_no = 1

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
            brand_page = get_brand_page(brand, header, str(page_no))
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
                return f"Status Code is {brand_page.status_code}.\nCould not access " + f"{brand} ".capitalize() + "\nBrand page may be available"
        # 1 get brand page
        page_no += 1
        products = []

        # Find all product containers (this selector may vary)
        product_links=soup.find_all('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        # print(product_links[0])

        for product in product_links:
            header = random.choice(headers)
            link = product.get('href')
            print(link)
            for a in range(200):
                pass
            product_link, product_page = get_product_page(link,header)
            if product_page.status_code == 200:
                product_page = BeautifulSoup(product_page.content, "html.parser")
            else:
                # exit function
                return products
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
                image_url = product_page.find("ul", {"class":"a-unordered-list a-nostyle a-horizontal list maintain-height"}).find("img")['src']
                print("image url", image_url)
                print(" ")
            except IndexError:
                continue
            except AttributeError:
                continue
            products.append({
                'name': name,
                'asin': asin,
                'page': page,
                'image_url': image_url
            })

def get_brand_page(brand,header,page_no):
    brand_url = "https://www.amazon.com/s?k=" + brand + "&page=" + page_no
    response = requests.get(brand_url, headers=header)
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
    import sys
    brand = sys.argv[1]
    print(scrape_amazon_product_list(brand))

    # header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0", "Accept-Language":"en-US, en:q=0.5"}
    # print(scrape_user_agents("https://www.useragents.me/",header))